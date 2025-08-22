CATEGORIES = ["dog_sitter","pet_sitter","babysitter"]

SCHEMAS = {
    "dog_sitter": {
        "required": ["pet_type","num_pets","feeding_schedule","vaccination_status"],
        "fields": {
            "pet_type": {"type":"string","enum":["dog","cat","other"]},
            "num_pets": {"type":"integer","min":1,"max":10},
            "feeding_schedule": {"type":"string","max_len":200},
            "vaccination_status": {"type":"boolean"}
        }
    },
    "pet_sitter": {
        "required": ["pet_type","visit_frequency"],
        "fields": {
            "pet_type": {"type":"string","enum":["dog","cat","bird","other"]},
            "visit_frequency": {"type":"integer","min":1,"max":6}
        }
    },
    "babysitter": {
        "required": ["children_count","age_group","first_aid"],
        "fields": {
            "children_count": {"type":"integer","min":1,"max":6},
            "age_group": {"type":"string","enum":["0-2","3-6","7-12","13+"]},
            "first_aid": {"type":"boolean"}
        }
    }
}
