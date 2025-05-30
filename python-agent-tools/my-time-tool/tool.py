# This file is the implementation of custom agent tool my-time-tool
from dataiku.llm.agent_tools import BaseAgentTool
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from utils.logging import logger


class TimeTool(BaseAgentTool):
    DEFAULT_TIMEZONE = "UTC"

    def set_config(self, config, plugin_config):
        self.config = config
        self.setup_logging()

    def setup_logging(self):
        """
        Sets up the logging level using the LazyLogger class.
        """
        logging_level = self.config.get("logging_level", "INFO")
        try:
            logger.set_level(logging_level)
            logger.info(f"Logging initialized with level: {logging_level}")
        except ValueError as e:
            logger.error(f"Invalid logging level '{logging_level}': {str(e)}")
            raise

    def get_descriptor(self, tool):
        logger.debug("Generating descriptor for the Time tool.")
        return {
            "description": "Get current time in a specific timezone or convert time between timezones",
            "inputSchema": {
                "$id": "https://dataiku.com/agents/tools/time/input",
                "title": "Input for the Time tool",
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["get_current_time", "convert_time"],
                        "description": "The action to perform (get_current_time or convert_time)"
                    },
                    "timezone": {
                        "type": "string",
                        "description": "IANA timezone name (e.g., 'America/New_York', 'Europe/London')",
                        "default": self.DEFAULT_TIMEZONE
                    },
                    "source_timezone": {
                        "type": "string",
                        "description": "Source IANA timezone name",
                        "default": self.DEFAULT_TIMEZONE
                    },
                    "time": {
                        "type": "string",
                        "description": "Time in 24-hour format (HH:MM) (required for convert_time)"
                    },
                    "target_timezone": {
                        "type": "string",
                        "description": "Target IANA timezone name",
                        "default": self.DEFAULT_TIMEZONE
                    }
                },
                "required": ["action"]
            }
        }

    def invoke(self, input, trace):
        args = input["input"]
        action = args["action"]

        logger.info(f"Invoking action: {action}")
        logger.debug(f"Input arguments: {args}")

        if action == "get_current_time":
            return self.get_current_time(args)
        elif action == "convert_time":
            return self.convert_time(args)
        else:
            logger.error(f"Invalid action: {action}")
            raise ValueError(f"Invalid action: {action}")

    def get_current_time(self, args):
        logger.debug("Starting 'get_current_time' action.")
        timezone_name = args.get("timezone", self.DEFAULT_TIMEZONE)
        logger.debug(f"Using timezone: {timezone_name}")

        try:
            timezone = ZoneInfo(timezone_name)
            current_time = datetime.now(timezone)
            logger.info(f"Current time in {timezone_name}: {current_time}")

            return {
                "output": {
                    "timezone": timezone_name,
                    "datetime": current_time.isoformat(),
                    "is_dst": bool(current_time.dst())
                }
            }
        except Exception as e:
            logger.error(f"Error getting current time: {str(e)}")
            raise

    def convert_time(self, args):
        logger.debug("Starting 'convert_time' action.")
        if "time" not in args:
            logger.error("Missing required field: time")
            raise ValueError("Missing required field: time")

        try:
            # Parse the input time
            try:
                time_obj = datetime.strptime(args["time"], "%H:%M").time()
            except ValueError:
                logger.error(f"Invalid time format: {args['time']}. Expected HH:MM")
                raise ValueError(f"Invalid time format: {args['time']}. Expected HH:MM")

            # Get timezones with defaults
            source_tz_name = args.get("source_timezone", self.DEFAULT_TIMEZONE)
            target_tz_name = args.get("target_timezone", self.DEFAULT_TIMEZONE)
            
            source_tz = ZoneInfo(source_tz_name)
            target_tz = ZoneInfo(target_tz_name)
            
            now = datetime.now(source_tz)
            source_time = datetime(
                now.year,
                now.month,
                now.day,
                time_obj.hour,
                time_obj.minute,
                tzinfo=source_tz
            )

            # Convert to target timezone
            target_time = source_time.astimezone(target_tz)
            
            # Calculate time difference
            source_offset = source_time.utcoffset() or timedelta()
            target_offset = target_time.utcoffset() or timedelta()
            hours_difference = (target_offset - source_offset).total_seconds() / 3600

            if hours_difference.is_integer():
                time_diff_str = f"{hours_difference:+.1f}h"
            else:
                time_diff_str = f"{hours_difference:+.2f}".rstrip("0").rstrip(".") + "h"

            logger.info(f"Time converted from {source_tz_name} to {target_tz_name}")

            return {
                "output": {
                    "source": {
                        "timezone": source_tz_name,
                        "datetime": source_time.isoformat(),
                        "is_dst": bool(source_time.dst())
                    },
                    "target": {
                        "timezone": target_tz_name,
                        "datetime": target_time.isoformat(),
                        "is_dst": bool(target_time.dst())
                    },
                    "time_difference": time_diff_str
                }
            }
        except Exception as e:
            logger.error(f"Error converting time: {str(e)}")
            raise
