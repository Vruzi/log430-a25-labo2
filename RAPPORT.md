# Labo 02 – Architecture monolithique, ORM, CQRS, Persistance polyglotte, DDD
<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann, Automne 2025.    

## Questions

> **Question 1** : Lorsque l'application démarre, la synchronisation entre Redis et MySQL est-elle initialement déclenchée par quelle méthode ? Veuillez inclure le code pour illustrer votre réponse.

La sunchronisation entre Redis et MySQl est lancé au début de l'applicaion quand on appelle le main dans store_manager.py
 ```python
 if __name__ == "__main__":
    try:
        print("----- Sync avec Redis -----")
        sync_all_orders_to_redis()
    except Exception as e:
        print(f"Erreur lors de la synchronisation avec Redis : {e}")
        print(e)
        
    server = HTTPServer(("0.0.0.0", 5000), StoreManager)
    print("Server running on http://0.0.0.0:5000")
    server.serve_forever()
 ``` 

> **Question 2** : Quelles méthodes avez-vous utilisées pour lire des données à partir de Redis ? Veuillez inclure le code pour illustrer votre réponse.
Pour lire des donnée avec Redis on peut utiliser r.keys pour aller chercher les clés du documents et ensuite puisque ces dernier sont en JSON on fait tout simplement json.load(r.get(key))

> **Question 3** : Quelles méthodes avez-vous utilisées pour ajouter des données dans Redis ? Veuillez inclure le code pour illustrer votre réponse.
Pour faire l'insertion avec Redis j'ai fait le code suivant:
```python
    order_data = {
        'id': order_id,
        'user_id': user_id,
        'total_amount': total_amount,
        'items': items
    }
    r.set(f"order:{order_id}", json.dumps(order_data))
```
J'ai utilise le set

> **Question 4** : Quelles méthodes avez-vous utilisées pour supprimer des données dans Redis ? Veuillez inclure le code pour illustrer votre réponse.
Pour faire la suppression avec Redis j'ai fait le code suivant:
```python
    r = get_redis_conn()
    r.delete(f"order:{order_id}")
```
J'ai utilisé le delete

> **Question 5** : Si nous souhaitions créer un rapport similaire, mais présentant les produits les plus vendus, les informations dont nous disposons actuellement dans Redis sont-elles suffisantes, ou devrions-nous chercher dans les tables sur MySQL ? Si nécessaire, quelles informations devrions-nous ajouter à Redis ? Veuillez inclure le code pour illustrer votre réponse.

Non c'est pour ça que j'ai utilisé MySQl car dans Redis il n'y à pas tout les données lors de la sync. Il y a des relations de table à faire avec product et user afin d'obtenir soit les noms d'utilisateur ou les nom de produit. Pour ce faire on peut utiliser ls query SQL `JOIN` afin d'arrivé à se résultat.
```python
def get_highest_spending_users():
    """Get report of best selling products"""
    # TODO: écrivez la méthode
    # triez le résultat par nombre de commandes (ordre décroissant)
    session = get_sqlalchemy_session()
    return session.query(
        User.id,
        User.name,
        func.sum(Order.total_amount).label('total_spent')
    ).join(Order, User.id == Order.user_id)\
        .group_by(User.id, User.name)\
        .order_by(func.sum(Order.total_amount).desc())\
        .limit(10)\
        .all()

def get_highest_sold_products():
    """Get report of best selling products"""
    session = get_sqlalchemy_session()
    return (
        session.query(
            Product.id,
            Product.name,
            func.sum(OrderItem.quantity).label("total_quantity"),
        )
        .select_from(Order)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .join(Product, Product.id == OrderItem.product_id)
        .group_by(Product.id, Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(10)
        .all()
    )
```
