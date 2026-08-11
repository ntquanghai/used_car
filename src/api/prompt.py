def create_prompt(
    row_id=None,
    year=None,
    manufacturer=None,
    model=None,
    description=None,
    condition=None,
    cylinders=None,
    fuel=None,
    transmission=None,
    drive=None,
    vehicle_type=None
):

    return f"""
You are an automotive information extraction assistant.

Complete the missing vehicle information using the inputs below.

Rules:
- Manufacturer and model are ground truth if already provided.
- Existing non-null values are verified and MUST NOT be changed.
- Return ALL fields, including existing ones.
- For existing values, copy them into the output and assign confidence 1.0.
- Only infer fields whose input value is null.
- Use the description, manufacturer, model and year together.
- If there is insufficient evidence, return null and confidence 0.0.
- Return ONLY valid JSON.

Vehicle

Year: {year}

Manufacturer: {manufacturer}

Model: {model}

Description:
{description}

Current verified values

Condition: {condition}
Cylinders: {cylinders}
Fuel: {fuel}
Transmission: {transmission}
Drive: {drive}
Type: {vehicle_type}

Allowed values

condition = [new, like new, excellent, good, fair, salvage]

cylinders = [
3 cylinders,
4 cylinders,
5 cylinders,
6 cylinders,
8 cylinders,
10 cylinders,
12 cylinders,
other
]

fuel = [
gas,
diesel,
hybrid,
electric,
other
]

transmission = [
automatic,
manual,
other
]

drive = [
fwd,
rwd,
4wd
]

type = [
sedan,
suv,
pickup,
truck,
coupe,
hatchback,
wagon,
van,
mini-van,
convertible,
offroad,
bus,
other
]

Return EXACTLY this JSON and nothing else:

{{
    "row_id": {row_id},
    "manufacturer": null,
    "manufacturer_confidence": 0.0,

    "model": null,
    "model_confidence": 0.0,

    "condition": null,
    "condition_confidence": 0.0,

    "cylinders": null,
    "cylinders_confidence": 0.0,

    "fuel": null,
    "fuel_confidence": 0.0,

    "transmission": null,
    "transmission_confidence": 0.0,

    "drive": null,
    "drive_confidence": 0.0,

    "type": null,
    "type_confidence": 0.0
}}
""".strip()