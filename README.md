https://simplifier.net/guide/uk-core-implementation-guide-stu3-sequence?version=1.7.0

intentional exclusions:
code-able concepts - only one, no text
text is ignored
datetimes - UTC only
the only allowed field in a Resource Reference is `reference`

incomplete:
- Observation -> Specimen
- Specimen -> ServiceRequest
- Slot -> Schedule

tested examples

* UKCore-AllergyIntolerance
* UKCore-Appointment
* UKCore-Composition
* UKCore-Condition
* UKCore-Consent
* UKCore-Device
* UKCore-DiagnosticReport
* UKCore-Encounter
* UKCore-EpisodeOfCare
* UKCore-FamilyMemberHistory
* UKCore-Flag
* UKCore-HealthcareService
* UKCore-ImagingStudy
* UKCore-Immunization
  * [Influenza Vaccine](tests/data/UKCore-Immunization-InfluenzaVaccine-Example.json)
* UKCore-List
* UKCore-Location
  * [Cardiology SJUH](tests/data/UKCore-Location-CardiologySJUH-Example.json)
  * [General Practice Nurse Clinic](tests/data/UKCore-Location-GeneralPracticeNurseClinic-Example.json)
  * [Hospital SJUH](tests/data/UKCore-Location-HospitalSJUH-Example.json)
* UKCore-Medication
  * [COVID-Vaccine](tests/data/UKCore-Medication-COVID-Vaccine-Example.json)
  * [Timolol VTM](tests/data/UKCore-Medication-TimololVTM-Example.json)
  * [Timoptol Eye Drops](tests/data/UKCore-Medication-TimoptolEyeDrops-Example.json)
* UKCore-MedicationAdministration
* UKCore-MedicationDispense
* UKCore-MedicationRequest
* UKCore-MedicationStatement
* UKCore-MessageHeader
* UKCore-Observation
  * [24 Hour Blood Pressure](tests/data/UKCore-Observation-24HourBloodPressure-Example.json)
  * [Awareness Of Diagnosis](tests/data/UKCore-Observation-AwarenessOfDiagnosis-Example.json)
  * [Breathing Normally](tests/data/UKCore-Observation-BreathingNormally-Example.json)
  * [Drug Use](tests/data/UKCore-Observation-DrugUse-Example.json)
  * [Fasting Test](tests/data/UKCore-Observation-FastingTest-Example.json)
  * [Finger Joint Inflamed](tests/data/UKCore-Observation-FingerJointInflamed-Example.json)
  * [Group Full Blood Count](tests/data/UKCore-Observation-Group-FullBloodCount-Example.json)
  * [Heavy Drinker](tests/data/UKCore-Observation-HeavyDrinker-Example.json)
  * [Lab Red Cell Count](tests/data/UKCore-Observation-Lab-RedCellCount-Example.json)
  * [Lab White Cell Count](tests/data/UKCore-Observation-Lab-WhiteCellCount-Example.json)
  * Vital-Signs
    * [BMI](tests/data/UKCore-Observation-VitalSigns-BMI-Example.json)
    * [Blood Pressure](tests/data/UKCore-Observation-VitalSigns-BloodPressure-Example.json)
    * [Body Height](tests/data/UKCore-Observation-VitalSigns-BodyHeight-Example.json)
    * [Body Temperature](tests/data/UKCore-Observation-VitalSigns-BodyTemperature-Example.json)
    * [Body Weight](tests/data/UKCore-Observation-VitalSigns-BodyWeight-Example.json)
    * [Head Circumference](tests/data/UKCore-Observation-VitalSigns-HeadCircumference-Example.json)
    * [Heart Rate](tests/data/UKCore-Observation-VitalSigns-HeartRate-Example.json)
    * [Oxygen Saturation](tests/data/UKCore-Observation-VitalSigns-OxygenSaturation-Example.json)
    * [Respiratory Rate](tests/data/UKCore-Observation-VitalSigns-RespiratoryRate-Example.json)
* UKCore-OperationOutcome
  * [Date Error](tests/data/UKCore-OperationOutcome-DateError-Example.json)
* UKCore-Organization
  * [Leeds Teaching Hospital](tests/data/UKCore-Organization-LeedsTeachingHospital-Example.json)
  * [White Rose Medical Centre](tests/data/UKCore-Organization-WhiteRoseMedicalCentre-Example.json)
* UKCore-Patient
  * [Baby Patient](tests/data/UKCore-Patient-BabyPatient-Example.json)
  * [Richard Smith](tests/data/UKCore-Patient-RichardSmith-Example.json)
* UKCore-Practitioner
  * [Consultant Sandra Gose](tests/data/UKCore-Practitioner-ConsultantSandraGose-Example.json)
  * [Doctor Paul Rastall](tests/data/UKCore-Practitioner-DoctorPaulRastall-Example.json)
  * [Pharmacist Jimmy Chuck](tests/data/UKCore-Practitioner-PharmacistJimmyChuck-Example.json)
* UKCore-PractitionerRole
  * [General Practitioner](tests/data/UKCore-PractitionerRole-GeneralPractitioner-Example.json)
* UKCore-Procedure
* UKCore-Questionnaire
* UKCore-QuestionnaireResponse
* UKCore-RelatedPerson
* UKCore-Schedule
  * [Immunization](tests/data/UKCore-Schedule-Immunization-Example.json)
* UKCore-ServiceRequest
* UKCore-Slot
  * [Available Walk-in Visit](tests/data/UKCore-Slot-AvailableWalkInVisit-Example.json)
* UKCore-Specimen
  * [Blood Specimen](tests/data/UKCore-Specimen-BloodSpecimen-Example.json)
  * [Urine Specimen](tests/data/UKCore-Specimen-UrineSpecimen-Example.json)
* UKCore-Task
