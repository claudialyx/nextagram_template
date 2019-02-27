from flask import Flask, redirect, render_template, url_for, flash, request, Blueprint
import braintree 
from app import app, gateway
from flask_login import current_user
from models.donation import Donation
from models.image import Image
from models.user import User
from helpers import email_notification


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

def generate_client_token():
    return gateway.client_token.generate()

def transact():
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)

@donations_blueprint.route('/checkouts/<id>/new', methods=['GET'])
def new_checkout(id):
    client_token = generate_client_token()
    return render_template('donations/new.html', client_token=client_token, id=id)

# Receive a payment method nonce from your client
@donations_blueprint.route("/checkout/<id>", methods=["POST"])
def create_checkout(id):
    # receiver = Image.get(Image.id==id).user_id
    # image_name = Image.get(Image.id==id).image_name
    image = Image.get_by_id(id)
    receiver = User.get_by_id(image.user_id)
    amount = request.form.get('amount')
    nonce_from_the_client = request.form["payment_method_nonce"]
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
        "submit_for_settlement": True
        }
    })

    if result.is_success and result.transaction:
        new_donation = Donation(amount=amount, image_id=id, donor_user_id=current_user.id)
        new_donation.save()
        email_notification(amount=amount, receiver=receiver, image_name=image.image_name)
        return redirect(url_for('donations.show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('users.show', username=receiver.username))


@donations_blueprint.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '.'
        }

    return render_template('donations/show.html', transaction=transaction, result=result)