"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template, get_param
from controllers.order_controller import get_report_highest_spending_users, get_report_best_sellers

def show_highest_spending_users():
    """ Show report of highest spending users """
    users = get_report_highest_spending_users()
    
    user_rows = [f"""
        <tr>
            <td>{i+1}</td>
            <td>{user.name}</td>
            <td>${user.total_spent}</td>
        </tr>""" for i, user in enumerate(users)]
    
    return get_template(f"""
        <h2>Les plus gros acheteurs</h2>
        <p>Classement des utilisateurs ayant le plus dépensé :</p>
        <table class="table">
            <tr>
                <th>Rang</th>
                <th>Utilisateur</th>
                <th>Total Dépensé</th>
            </tr>
            {" ".join(user_rows)}
        </table>
        <p><a href="/">← Retour aux rapports</a></p>
    """)

def show_best_sellers():
    """ Show report of best selling products """
    products = get_report_best_sellers()
    
    product_rows = [f"""
        <tr>
            <td>{i+1}</td>
            <td>{product.name}</td>
            <td>{product.total_quantity}</td>
        </tr>""" for i, product in enumerate(products)]
    
    return get_template(f"""
        <h2>Les articles les plus vendus</h2>
        <p>Classement des produits vendus en plus grande quantité :</p>
        <table class="table">
            <tr>
                <th>Rang</th>
                <th>Produit</th>
                <th>Quantité Vendue</th>
            </tr>
            {" ".join(product_rows)}
        </table>
        <p><a href="/">← Retour aux rapports</a></p>
    """)
