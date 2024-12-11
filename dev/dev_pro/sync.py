
from datetime import timedelta

from django.db import transaction
from django.utils.timezone import now
from .models import *
#
# def sync_databases():
#     # Define cutoff date for the last 30 days
#     cutoff_date = now() - timedelta(days=30)
#     print('Cutoff date:', cutoff_date)
#
#     # Step 1: Sync `patient_details` from default to fallback
#     recent_patients = Patientsdetails.objects.using('default').filter(updated_at__gte=cutoff_date)
#     print('Recent patients:', recent_patients)
#     for patient in recent_patients:
#         # Update or create in fallback database
#         fallback_patient, created = Patientsdetails.objects.using('fallback').update_or_create(
#             id=patient.id,  # Match by ID to ensure consistency
#             defaults={
#                 'patient_name': patient.patient_name,
#                 'age': patient.age,
#                 'gender':patient.gender,
#                 'procedure': patient.procedure,
#                 'mobile': patient.mobile,
#                 'patient_email':patient.patient_email,
#                 'referred': patient.referred,
#                 'updated_at': patient.updated_at,
#             }
#         )
#         print(f'Patient {"created" if created else "updated"}: {fallback_patient}')
#
#     # Step 2: Delete old `patient_details` from fallback
#     deleted_patients = Patientsdetails.objects.using('fallback').filter(updated_at__lt=cutoff_date).delete()
#     print(f'Deleted old patients: {deleted_patients}')
#
#     # Step 3: Sync `reports_details` from default to fallback
#     recent_reports = Patientreports.objects.using('default').filter(date__gte=cutoff_date)
#     print('Recent reports:', recent_reports)
#     for report in recent_reports:
#         print('report',report.patient_details_id)
#         print('report idd',report.patient_details_id.id)
#         # Ensure the referenced patient exists in the fallback database
#         try:
#             fallback_patient = Patientsdetails.objects.using('fallback').get(id=report.patient_details_id.id)
#             print('fallback_patient',fallback_patient)
#             print('fallback_patient typt',type(fallback_patient))
#             print('fallback_patientiddd',fallback_patient.id)
#             print('fallback_patientiddd',type(fallback_patient.id))
#
#             # Update or create in fallback database
#             fallback_report, created = Patientreports.objects.using('fallback').update_or_create(
#                 id=report.id,
#                 defaults={
#                     'patient_details_id_id': fallback_patient.id,  # Use the primary key instead of the object
#                     'report_file': report.report_file,
#                     'date': report.date,
#                     'time': report.time,
#
#                 }
#             )
#             print(f'Report {"created" if created else "updated"}: {fallback_report}')
#         except Patientsdetails.DoesNotExist:
#             print(f"Skipping report {report.id} because related patient does not exist in fallback.")
#
#
#     # Step 4: Delete old `reports_details` from fallback
#     deleted_reports = Patientreports.objects.using('fallback').filter(date__lt=cutoff_date).delete()
#     print(f'Deleted old reports: {deleted_reports}')
#









def sync_databases():
    """Sync data from fallback to default database."""

    # Step 1: Sync `New_patient_details` from fallback to default
    new_patients = NewPatientsdetails.objects.using('fallback').all()
    patient_mapping = {}  # Map fallback patient IDs to default patient objects
    print('new_patients',new_patients)
    for new_patient in new_patients:
        print('new_patient',new_patient)
        print('fallbak id j ',new_patient.id)
        try:
            # Match patient in the default database by `email_id` or `mobile_name`
            existing_patient = Patientsdetails.objects.using('default').filter(
                patient_email=new_patient.patient_email
            ).first() or Patientsdetails.objects.using('default').filter(
                mobile=new_patient.mobile
            ).first()
            print('existing_patient',existing_patient)

            if existing_patient:
                global patient_obj
                # Update existing patient details if found

                # existing_patient.patient_name = new_patient.patient_name
                # existing_patient.age = new_patient.age
                # existing_patient.gender = new_patient.gender
                # existing_patient.procedure = new_patient.procedure
                # existing_patient.mobile = new_patient.mobile
                # existing_patient.patient_email = new_patient.patient_email
                # existing_patient.referred = new_patient.referred
                existing_patient.updated_at = new_patient.updated_at or now()
                existing_patient.save(using='default')
                print(f"Existing patient updated: {existing_patient}")
                patient_obj = existing_patient
            else:
                print("else")
                # Create a new patient in the default database
                patient_obj = Patientsdetails.objects.using('default').create(
                    patient_name=new_patient.patient_name,
                    age=new_patient.age,
                    gender=new_patient.gender,
                    procedure=new_patient.procedure,
                    mobile=new_patient.mobile,
                    patient_email=new_patient.patient_email,
                    referred=new_patient.referred,
                    updated_at=new_patient.updated_at or now(),

                )
                print(f"New patient created: {patient_obj}")
            print(f"N...........................: {patient_obj.id}")




            # Save the mapping between fallback and default IDs
            # patient_mapping[new_patient.id] = patient_obj
            patient_obj.save()

        except Exception as e:
            print(f"Error syncing patient {new_patient.id}: {e}")

    # Step 2: Sync `new_reports_details` from fallback to default
    new_reports = NewPatientreports.objects.using('fallback').all()
    print('new_reports',new_reports)

    for new_report in new_reports:
        # NewPatientreports.objects.using('fallback').update(patient_details_id=)


        # default_pd_query=Patientsdetails.objects.using('default').get(id=new_report.patient_details_id.id)
        # print('default_pd_query',default_pd_query)


        try:
            # Use the patient mapping to get the corresponding patient in the default database
            # default_patient = default_pd_query.id
            print('default_patient',default_patient)

            # if not default_patient:
            #     print(f"Skipping report {new_report.id} because related patient does not exist in default.")
            #     continue

            # Create the report in the default database
            report_obj = Patientreports.objects.using('default').create(
                patient_details_id_id=default_patient,
                report_file=new_report.report_file,
                date=new_report.date,
                time=new_report.time,
            )
            print(f"New report created: {report_obj}")
        except Exception as e:
            print(f"Error syncing report {new_report.id}: {e}")

    # Step 3: Delete synced records from fallback database
    try:
        with transaction.atomic(using='fallback'):
            # Delete all synced patients and reports from the fallback database
            NewPatientsdetails.objects.using('fallback').all().delete()
            NewPatientreports.objects.using('fallback').all().delete()
            print("Deleted synced records from fallback database.")
    except Exception as e:
        print(f"Error deleting records from fallback: {e}")