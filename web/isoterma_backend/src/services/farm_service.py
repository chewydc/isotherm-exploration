import json
import logging
from typing import List, Optional
from pathlib import Path

from src.models.farm_models import Farm

logger = logging.getLogger(__name__)

class FarmService:
    """Service for farm data management"""
    
    DATA_FILE = Path(__file__).parent.parent.parent / "data" / "fincas.json"
    
    @staticmethod
    def get_all_farms() -> List[Farm]:
        """Get all farms from JSON file"""
        try:
            with open(FarmService.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            farms = [Farm(**farm_data) for farm_data in data]
            logger.info(f"Loaded {len(farms)} farms")
            return farms
            
        except FileNotFoundError:
            logger.error(f"Farms data file not found: {FarmService.DATA_FILE}")
            return []
        except Exception as e:
            logger.error(f"Error loading farms: {e}")
            return []
    
    @staticmethod
    def get_farm_by_id(farm_id: str) -> Optional[Farm]:
        """Get specific farm by ID"""
        farms = FarmService.get_all_farms()
        for farm in farms:
            if farm.id == farm_id:
                logger.info(f"Found farm: {farm.name}")
                return farm
        
        logger.warning(f"Farm not found: {farm_id}")
        return None