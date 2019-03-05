import re


def balance():
    equation = re.sub(r'\s', '', input('Enter Your Skeleton Equation: ').replace(r'\s', ''))
    if '->' not in equation:
        print('Invalid Equation')
        return
    elements = equation.split('->')
    elements[0] = elements[0].split('+')
    elements[1] = elements[1].split('+')
    for group_index in range(0, len(elements)):
        for compound_index in range(0, len(elements[group_index])):
            elements[group_index][compound_index] = split(elements[group_index][compound_index])
            for element_index in range(0, len(elements[group_index][compound_index])):
                elements[group_index][compound_index][element_index] = \
                    enumerate_element(elements[group_index][compound_index][element_index])
    reactants = elements[0]
    products = elements[1]
    reactant_element_quantities = {}
    product_element_quantities = {}
    reactant_coefficients = [1] * len(reactants)
    product_coefficients = [1] * len(products)
    calculate_quantities(reactants, reactant_coefficients, reactant_element_quantities)
    calculate_quantities(products, product_coefficients, product_element_quantities)
    if reactant_element_quantities == product_element_quantities:
        print('Equation is Already Balanced')
        return
    if set(reactant_element_quantities.keys()) != set(product_element_quantities.keys()):
        print('Equation Cannot Be Balanced')
        return
    system_coefficients = []
    system_sums = []
    for element in reactant_element_quantities.keys()


def calculate_quantities(compounds, coefficients, quantities):
    for reactant_index in range(0, len(compounds)):
        for element_index in range(0, len(compounds[reactant_index])):
            if compounds[reactant_index][element_index]['element_name'] not in quantities:
                quantities[compounds[reactant_index][element_index]['element_name']] = \
                    compounds[reactant_index][element_index]['quantity']
            else:
                quantities[compounds[reactant_index][element_index]['element_name']] += \
                    compounds[reactant_index][element_index]['quantity'] * coefficients[reactant_index]


def split(compound: str):
    result = []
    sub_start = 0
    for index in range(1, len(compound)):
        if compound[index].istitle():
            result.append(compound[sub_start: index])
            sub_start = index
    result.append(compound[sub_start:])
    return result


def enumerate_element(element: str):
    element_name = re.split(r'\d', element)[0]
    quantity = re.split(r'[A-z]+', element)[-1]
    if quantity == '':
        quantity = 1
    return {'element_name': element_name, 'quantity': int(quantity)}


if __name__ == '__main__':
    balance()
