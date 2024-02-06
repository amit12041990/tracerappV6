from flask import request, redirect, url_for, jsonify, session
import uuid
from datetime import datetime
from model.model import ChildModel
def generate_5_digit_unique_id(unique_id):
    # Generate a UUID
    unique_id = unique_id

    # Extract the hexadecimal portion from the UUID
    hex_portion = unique_id.replace("-", "")[:5]

    # Convert the hexadecimal portion to an integer
    five_digit_portion = int(hex_portion, 16)

    # Modulo to ensure the result is a 5-digit number
    five_digit_portion %= 100000

    return five_digit_portion

def crud_add_child():
    if request.method == 'POST':
        currentCollection = ChildModel()
        formdata = request.form

        if formdata['formName'] == 'add-child':
            gender = formdata['gender']
            dob = formdata['dob']
            childName = formdata['childName']
            unique_id = str(uuid.uuid4())
            app_id = generate_5_digit_unique_id(unique_id)
            ref_email = session['username']

            try:
                created_date = datetime.now().strftime("%c")
                child_data = {
                    'name': childName,
                    'gender': gender,
                    'ref_id': ref_email,
                    'u_id': unique_id,
                    'dob': dob,
                    'mobile_id':str(app_id)
                }
                db_response = currentCollection.add_child(child_data)
                if db_response:
                    return redirect(url_for('hello_tracer'))
            except Exception as ex:
                print(ex)
                return jsonify(ex), 500

        elif formdata['formName'] == 'edit-child':
            child_Id = formdata['child_id']
            childName = formdata['childName']
            gender = formdata['gender']
            dob = formdata['dob']
            
            updated_data = {
                'name': childName,
                'gender': gender,
                'dob': dob
            }
            
            try:
                update = currentCollection.edit_child(child_Id, updated_data)
                if update:
                    return redirect(url_for('hello_tracer'))
            except Exception as ex:
                print(ex)
                return jsonify(ex), 500

        elif formdata['formName'] == 'delete-child':
            try:
                delete_child = currentCollection.delete_child(formdata['child_id'])
                if delete_child:
                    return redirect(url_for('hello_tracer'))
            except Exception as ex:
                print(ex)
                return jsonify(ex), 500

    return jsonify(formdata)
