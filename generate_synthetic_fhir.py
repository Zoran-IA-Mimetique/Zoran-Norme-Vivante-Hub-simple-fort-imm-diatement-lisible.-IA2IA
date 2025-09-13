# Generate small synthetic FHIR-like samples (placeholder).
import json, hashlib
samples = []
for i in range(5):
    pid = f"pat-{i:03d}"
    samples.append({
        "id": pid,
        "pid": "phi::"+hashlib.sha256(pid.encode()).hexdigest()[:24],
        "birthDate": "1970-01-01",
        "sex": "other",
        "postcode": "00000",
        "equitySegments": ["rural_low_income"]
    })
print(json.dumps(samples, indent=2))
