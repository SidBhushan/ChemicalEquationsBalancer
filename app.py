import re
from math import gcd
from numpy.linalg import solve as solve_linear_equation
from fractions import Fraction


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
    for element in reactant_element_quantities.keys():
        system_sums.append(find_quantity_of(element, reactants[0]))
        equation = []
        for index in range(1, len(reactants)):
            equation.append(-1 * find_quantity_of(element, reactants[index]))
        for index in range(0, len(products)):
            equation.append(find_quantity_of(element, products[index]))
        system_coefficients.append(equation)
    solution = solve_linear_equation(system_coefficients, system_sums)
    solution_fractions = []
    for coefficient in solution:
        solution_fractions.append(Fraction(coefficient).limit_denominator())
    common_denominator = gcd_list(list(filter(lambda x: x != -1, map(lambda fraction: fraction.denominator if fraction.denominator != 1 else -1, solution_fractions))))
    integer_solution = list(map(lambda fraction: (fraction * common_denominator).numerator, solution_fractions))
    balanced_coefficients = [common_denominator]
    for coefficient in integer_solution:
        balanced_coefficients.append(coefficient)
    balanced_equation = f'{format_equation(balanced_coefficients, reactants)}->{format_equation(balanced_coefficients[len(reactants):], products)}'
    print(f'Balanced Equation: {balanced_equation}')


def format_equation(coefficients: list, compounds: list):
    result = ''
    for compound_index in range(0, len(compounds)):
        result += str(coefficients[compound_index]) if coefficients[compound_index] != 1 else ''
        for element in compounds[compound_index]:
            result += element['element_name'] + (str(element['quantity']) if element['quantity'] != 1 else '')
        result += '+'
    return result[:-1]


def gcd_list(input_list: list):
    if len(input_list) == 0:
        return 1
    result = input_list[0]
    for item in input_list:
        result = gcd(result, item)
    return result


def find_quantity_of(element: str, compound: list):
    for compound_element in compound:
        if compound_element['element_name'] == element:
            return compound_element['quantity']
    return 0


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
