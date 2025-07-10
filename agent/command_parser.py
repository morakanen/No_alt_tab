"""
Command parser for matching speech transcripts to commands
"""
import json
import os
import logging
import importlib
from difflib import get_close_matches

logger = logging.getLogger("game-agent")

class CommandParser:
    def __init__(self, vocabulary_path=None):
        """
        Initialize the command parser with a vocabulary of commands
        
        Args:
            vocabulary_path: Path to the JSON file containing command vocabulary
        """
        self.commands = {}
        self.phrases_to_handlers = {}
        
        if vocabulary_path is None:
            # Default path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            vocabulary_path = os.path.join(current_dir, "commands", "command_vocabulary.json")
        
        self.load_vocabulary(vocabulary_path)
    
    def load_vocabulary(self, vocabulary_path):
        """
        Load command vocabulary from a JSON file
        
        Args:
            vocabulary_path: Path to the JSON file containing command vocabulary
        """
        try:
            with open(vocabulary_path, 'r') as f:
                vocabulary = json.load(f)
            
            for cmd in vocabulary.get("commands", []):
                handler = cmd.get("handler")
                phrases = cmd.get("phrases", [])
                description = cmd.get("description", "")
                
                self.commands[handler] = {
                    "phrases": phrases,
                    "description": description
                }
                
                # Create a mapping from each phrase to its handler
                for phrase in phrases:
                    self.phrases_to_handlers[phrase.lower()] = handler
            
            logger.info(f"Loaded {len(self.commands)} commands with {len(self.phrases_to_handlers)} phrases")
        except Exception as e:
            logger.error(f"Failed to load command vocabulary: {e}")
            # Initialize with empty commands if file can't be loaded
            self.commands = {}
            self.phrases_to_handlers = {}
    
    def normalize_text(self, text):
        """
        Normalize text by converting to lowercase and removing extra whitespace
        
        Args:
            text: Text to normalize
        
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        return text
    
    def parse_command(self, transcript, fuzzy_match=True, threshold=0.6):
        """
        Parse a transcript and match it to a command
        
        Args:
            transcript: Speech transcript to parse
            fuzzy_match: Whether to use fuzzy matching
            threshold: Threshold for fuzzy matching (0-1)
        
        Returns:
            Tuple of (handler_name, confidence) or (None, 0) if no match
        """
        if not transcript:
            return None, 0
        
        normalized = self.normalize_text(transcript)
        
        # First try exact matching
        for phrase, handler in self.phrases_to_handlers.items():
            if phrase in normalized:
                logger.info(f"Exact match found: '{phrase}' -> {handler}")
                return handler, 1.0
        
        # If no exact match and fuzzy matching is enabled
        if fuzzy_match:
            # Get all phrases as a list
            all_phrases = list(self.phrases_to_handlers.keys())
            
            # Try to find close matches
            matches = get_close_matches(normalized, all_phrases, n=1, cutoff=threshold)
            
            if matches:
                best_match = matches[0]
                handler = self.phrases_to_handlers[best_match]
                # Calculate a simple confidence score based on string similarity
                confidence = sum(c1 == c2 for c1, c2 in zip(normalized, best_match)) / max(len(normalized), len(best_match))
                logger.info(f"Fuzzy match found: '{normalized}' ~ '{best_match}' -> {handler} (confidence: {confidence:.2f})")
                return handler, confidence
        
        logger.info(f"No command match found for: '{normalized}'")
        return None, 0
    
    def execute_command(self, handler_name, command_text=""):
        """
        Dynamically imports and executes the specified command handler.
        
        Args:
            handler_name (str): Name of the handler module to execute
            command_text (str): Original command text for context-aware handlers
            
        Returns:
            str: Result message from the handler
        """
        try:
            # Import the handler module dynamically
            handler_module = importlib.import_module(f"agent.commands.{handler_name}")
            
            # Execute the handler with the original command text
            if hasattr(handler_module, "execute"):
                return handler_module.execute(command_text=command_text)
            else:
                logger.error(f"Handler {handler_name} does not have an execute function")
                return f"Error: Handler {handler_name} is not properly implemented"
        except Exception as e:
            logger.error(f"Error executing command handler {handler_name}: {e}")
            return f"Error executing command: {e}"
