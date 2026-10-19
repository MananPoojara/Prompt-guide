def search_products(products, query):
    """Return matching product names in their original order."""
    return [name for name in products if query in name]
