from fastapi import APIRouter, HTTPException
import logging

from src.services.farm_service import FarmService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/farms", tags=["Farms"])

@router.get("")
async def get_all_farms():
    """Get all farms"""
    try:
        farms = FarmService.get_all_farms()
        return {
            "success": True,
            "farms": farms
        }
    except Exception as e:
        logger.error(f"Error in get_all_farms: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{farm_id}")
async def get_farm_detail(farm_id: str):
    """Get farm details by ID"""
    try:
        farm = FarmService.get_farm_by_id(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail=f"Farm not found: {farm_id}")
        
        return {
            "success": True,
            "farm": farm
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_farm_detail: {e}")
        raise HTTPException(status_code=500, detail=str(e))