https://simplifier.net/guide/uk-core-implementation-guide-stu3-sequence?version=1.7.0

* UKCore-AllergyIntolerance ✅
* UKCore-Appointment ✅
* UKCore-Composition ✅ [2, 4]
* UKCore-Condition ✅
* UKCore-Consent ✅
* UKCore-Device ✅
* UKCore-DiagnosticReport ✅
* UKCore-Encounter ✅
* UKCore-EpisodeOfCare ✅
* UKCore-FamilyMemberHistory ✅
* UKCore-Flag ✅
* UKCore-HealthcareService
* UKCore-ImagingStudy ✅
* UKCore-Immunization ✅
* UKCore-List ✅
* UKCore-Location ✅
* UKCore-Medication ✅
* UKCore-MedicationAdministration ❌
* UKCore-MedicationDispense ❌
* UKCore-MedicationRequest ✅
* UKCore-MedicationStatement ❌
* UKCore-MessageHeader ✅ [4]
* UKCore-Observation ✅
* UKCore-OperationOutcome ✅
* UKCore-Organization ✅
* UKCore-Patient ✅
* UKCore-Practitioner ✅
* UKCore-PractitionerRole ✅
* UKCore-Procedure ✅
* UKCore-Questionnaire ✅
* UKCore-QuestionnaireResponse ❌
* UKCore-RelatedPerson ✅
* UKCore-Schedule ✅
* UKCore-ServiceRequest ✅
* UKCore-Slot ✅
* UKCore-Specimen ✅
* UKCore-Task ✅

## intentional exclusions
fhirlight does not support the full UK-Core specification. Generally this is because the cost of some features outweighs
the benefits.

### Codeable-Concepts
1. Codeable-Concepts will only ever have one coding. The reason for this is that the cost of having many join
tables is high, and the benefit of being able to encode the same thing two different ways is low.

i.e. POSTing the following would result in an error because there are two encodings:
```json
"code" : {
  "coding":  [
    {
      "system": "http://snomed.info/sct",
      "code": "60621009",
      "display": "Body mass index"
    },
    {
      "system": "http://loinc.org",
      "code": "39156-5",
      "display": "Body mass index (BMI) [Ratio]"
    }
  ]
}
```

but the following would be legitimate.
```json
"code": {
  "coding":  [
    {
      "system": "http://snomed.info/sct",
      "code": "60621009",
      "display": "Body mass index"
    }
  ]
}
```

### text
Generally `text` fields are not supported.

### datetimes
Only ISO DateTimes are supported and they will always be rendered as UTC by the API. 

### references
The only reference type supported is:
```json
{"reference": "<type>/<identifier>"}
```
all other fields such as `type`, `identifier`, `display` are not allowed and will result in an error. Note that this 
means that it is not possible to reference an external entity.
)
