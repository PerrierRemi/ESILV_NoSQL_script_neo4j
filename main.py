import json
import csv

# CONSTANTS
NULL_VALUES = ['', None, 'null', [], {}]
FORBIDEN_CHARS = ['\\', '\'', '\"']
# Nodes
VAR_COMPANIES = ['name', 'permalink', 'crunchbase_url', 'homepage_url',
                 'blog_url', 'blog_feed_url', 'twitter_username', 'twitter_username',
                 'number_of_employees', 'founded_year', 'founded_month', 'founded_day',
                 'deadpooled_year', 'deadpooled_month', 'deadpooled_day', 'deadpooled_url',
                 'email_address', 'phone_number', 'description', 'created_at', 'updated_at',
                 'total_money_raised']
VAR_PRODUCTS = ['name', 'permalink']
VAR_PERSONS = ['first_name', 'last_name', 'permalink']
# Relationships
VAR_COMPANIES_PERSONS = ['is_past', 'title']


def create_files():
    # Files
    data = open('data.json', 'r', encoding='utf-8')
    companies_file = open('companies.csv', 'w', encoding='utf-8')
    products_file = open('products.csv', 'w', encoding='utf-8')
    persons_file = open('persons.csv', 'w', encoding='utf-8')
    companies_products_file = open(
        'companies_products.csv', 'w', encoding='utf-8')
    companies_competitors_file = open(
        'companies_competitors.csv', 'w', encoding='utf-8')
    companies_persons_file = open(
        'companies_persons.csv', 'w', encoding='utf-8')

    # Writers and headlines
    companies_writer = csv.writer(companies_file)
    companies_writer.writerow(VAR_COMPANIES)

    products_writer = csv.writer(products_file)
    products_writer.writerow(VAR_PRODUCTS)

    persons_writer = csv.writer(persons_file)
    persons_writer.writerow(VAR_PERSONS)

    companies_products_writer = csv.writer(companies_products_file)
    companies_products_writer.writerow(
        ['companie_permalink', 'product_permalink'])

    companies_competitors_writer = csv.writer(companies_competitors_file)
    companies_competitors_writer.writerow(
        ['companie_permalink', 'competitor_permalink'])

    comapnies_persons_writer = csv.writer(companies_persons_file)
    comapnies_persons_writer.writerow(
        ['companie_permalink', 'person_permalink'] + VAR_COMPANIES_PERSONS)

    # Read data and write to csv
    # Unique identifiers
    products_permalinks = []
    persons_permalinks = []

    line = data.readline()
    while line:
        json_companie = json.loads(line)
        # Companies
        csv_companie = format(json_companie, VAR_COMPANIES)
        companies_writer.writerow(csv_companie)

        # Products
        if 'products' in json_companie:
            for product in json_companie['products']:
                # Node
                if product['permalink'] not in products_permalinks:
                    csv_product = format(product, VAR_PRODUCTS)
                    products_writer.writerow(csv_product)
                    products_permalinks.append(product['permalink'])
                # Relationship
                csv_companie_product = [
                    json_companie['permalink'], product['permalink']]
                companies_products_writer.writerow(csv_companie_product)

        # Persons
        if 'relationships' in json_companie:
            for relationship in json_companie['relationships']:
                # Node
                if relationship['person']['permalink'] not in persons_permalinks:
                    csv_person = format(relationship['person'], VAR_PERSONS)
                    persons_writer.writerow(csv_person)
                    persons_permalinks.append(
                        relationship['person']['permalink'])
                # Relationship
                csv_companie_person = [json_companie['permalink'], relationship['person']
                                       ['permalink']] + format(relationship, VAR_COMPANIES_PERSONS)
                comapnies_persons_writer.writerow(csv_companie_person)

        # Competitors
        if 'competitions' in json_companie:
            for competitions in json_companie['competitions']:
                csv_companie_competitor = [
                    json_companie['permalink'], competitions['competitor']['permalink']]
                companies_competitors_writer.writerow(csv_companie_competitor)
        line = data.readline()

    # Close all files
    data.close()
    companies_file.close()
    products_file.close()
    persons_file.close()
    companies_products_file.close()
    companies_competitors_file.close()
    companies_persons_file.close()


def format(dictionary, var_array):
    # Format value to csv
    line = []
    for var in var_array:
        if not var in dictionary:
            line.append('N/A')
        elif dictionary[var] in NULL_VALUES:
            line.append('N/A')
        elif type(dictionary[var]) == str:
            s = dictionary[var]
            for char in FORBIDEN_CHARS:
                s = s.replace(char, '')
            line.append(s)
        else:
            line.append(dictionary[var])
    return line

 # Call main
create_files()
