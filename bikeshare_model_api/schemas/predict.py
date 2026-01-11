from typing import Any, List, Optional

from pydantic import BaseModel
from bikeshare_model.processing.validation import DataInputSchema


class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    #predictions: Optional[List[int]]
    predictions: Optional[int]
    
class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]
    
    class Config:
        schema_extra = {
            "example": {
                "inputs": [ 
                    {
                        "dteday": "2012-11-6",
                        "season": "winter",
                        "hr": "6pm",
                        "holiday": "No",
                        "weekday": "Tue",
                        "workingday": "Yes",
                        "weathersit": "Clear",
                        "temp": 16,
                        "atemp": 17.5,
                        "hum": 30,
                        "windspeed": 10
                    }
                ]
                
            }
        }   