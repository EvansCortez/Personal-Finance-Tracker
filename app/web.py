# app/web.py

from flask import Flask, request, render_template_string, send_file
import core

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server environments
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Finance Tracker</title>
<style>
  body {
    font-family: Arial, sans-serif;
    margin: 40px;
    /* Solid color background: */
    background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%);
    /* Or use an image background instead:
    background: url('https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80') no-repeat center center fixed;
    background-size: cover;
    */
  }
  table { border-collapse: collapse; width: 60%; }
  th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
  th { background: #f2f2f2; }
  input[type=text], input[type=number] { width: 200px; }
  form { margin-bottom: 20px; }
  .action-btn { margin-right: 5px; }
</style>
<h2>Set Initial Balance</h2>
<form method="post" action="/set_balance">
  Initial Balance: <input name="initial_balance" type="number" step="0.01" value="{{ initial_balance }}">
  <input type="submit" value="Set">
</form>
<h2>Add Transaction</h2>
<form method=post>
  Date: <input name="date" type="text" placeholder="YYYY-MM-DD" value="{{ edit_data.date if edit_data else '' }}"><br>
  Category: <input name="category" type="text" value="{{ edit_data.category if edit_data else '' }}"><br>
  Amount: <input name="amount" type="number" step="0.01" value="{{ edit_data.amount if edit_data else '' }}"><br>
  Description: <input name="description" type="text" value="{{ edit_data.description if edit_data else '' }}"><br>
  {% if edit_index is not none %}
    <input type="hidden" name="edit_index" value="{{ edit_index }}">
    <input type=submit value="Update">
    <a href="/" class="action-btn">Cancel</a>
  {% else %}
    <input type=submit value="Add">
  {% endif %}
</form>
<h2>Initial Balance: ${{ "{:,.2f}".format(initial_balance) }}</h2>
<h2>Net Savings: ${{ "{:,.2f}".format(net) }}</h2>
<h2>Transactions</h2>
<table>
  <tr><th>Date</th><th>Category</th><th>Amount</th><th>Description</th><th>Actions</th></tr>
  {% for t in transactions %}
    <tr>
      <td>{{ t[0] }}</td>
      <td>{{ t[1] }}</td>
      <td>{{ t[2] }}</td>
      <td>{{ t[3] }}</td>
      <td>
        <form method="post" action="/delete" style="display:inline;">
          <input type="hidden" name="index" value="{{ loop.index0 }}">
          <button type="submit" class="action-btn">Delete</button>
        </form>
        <form method="get" action="/edit" style="display:inline;">
          <input type="hidden" name="index" value="{{ loop.index0 }}">
          <button type="submit" class="action-btn">Edit</button>
        </form>
      </td>
    </tr>
  {% endfor %}
</table>
<h2>Spending Report</h2>
<img src="/report.png">
"""

@app.route('/set_balance', methods=['POST'])
def set_balance():
    try:
        amount = float(request.form['initial_balance'])
        core.set_initial_balance(amount)
    except ValueError:
        pass
    return '', 303, {'Location': '/'}

@app.route('/delete', methods=['POST'])
def delete():
    index = int(request.form['index'])
    core.delete_transaction(index)
    return '', 303, {'Location': '/'}

@app.route('/edit', methods=['GET'])
def edit():
    index = int(request.args['index'])
    transactions = core.get_transactions()
    t = transactions[index]
    edit_data = {
        'date': t[0],
        'category': t[1],
        'amount': t[2],
        'description': t[3]
    }
    net = core.calculate_net_savings()
    initial_balance = core.get_initial_balance()
    # Format amounts as currency strings
    formatted_transactions = []
    for i, t in enumerate(transactions):
        try:
            amount_str = "${:,.2f}".format(float(t[2]))
        except (ValueError, IndexError):
            amount_str = t[2]
        formatted_transactions.append([t[0], t[1], amount_str, t[3]])
    return render_template_string(
        TEMPLATE,
        net=net,
        transactions=formatted_transactions,
        edit_data=edit_data,
        edit_index=index,
        initial_balance=initial_balance
    )

@app.route('/report.png')
def report():
    # Generate pie chart using category totals
    category_totals = core.get_category_totals()
    fig, ax = plt.subplots()
    if category_totals:
        ax.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
        ax.set_title("Spending by Category")
    else:
        ax.text(0.5, 0.5, "No data", ha='center', va='center')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        edit_index = request.form.get('edit_index')
        if edit_index is not None and edit_index != '':
            # Edit transaction
            core.edit_transaction(
                int(edit_index),
                request.form['date'],
                request.form['category'],
                request.form['amount'],
                request.form['description']
            )
        else:
            # Add transaction
            core.add_transaction(
                request.form['date'],
                request.form['category'],
                request.form['amount'],
                request.form['description']
            )
    net = core.calculate_net_savings()
    initial_balance = core.get_initial_balance()
    transactions = core.get_transactions()
    # Format amounts as currency strings
    formatted_transactions = []
    for t in transactions:
        try:
            amount_str = "${:,.2f}".format(float(t[2]))
        except (ValueError, IndexError):
            amount_str = t[2]
        formatted_transactions.append([t[0], t[1], amount_str, t[3]])
    return render_template_string(
        TEMPLATE,
        net=net,
        transactions=formatted_transactions,
        edit_data=None,
        edit_index=None,
        initial_balance=initial_balance
    )

if __name__ == '__main__':
    app.run(debug=True)
