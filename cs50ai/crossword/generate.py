import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Test word length for all domains in variables
        for variable in self.domains:
            temp = copy.deepcopy(self.domains[variable])
            for word in temp:
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Compare variables with overlap only
        if self.crossword.overlaps[x, y] != None:
            overlap = self.crossword.overlaps[x, y]
            
            # Get overlap letters from words in domain of y
            letters = []
            for word in self.domains[y]:
                letters.append(word[overlap[1]])
            
            # Compare if words in domain of x do not match any overlap letter
            temp = copy.deepcopy(self.domains[x])
            for word in temp:
                if word[overlap[0]] not in letters:
                    self.domains[x].remove(word)

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Enforce arc consistency across domains
        while True:
            values_before = 0
            for variable in self.domains:
                values_before += len(self.domains[variable])
            
            for variable1 in self.domains:
                for variable2 in self.domains:
                    if variable1 != variable2:
                        self.revise(variable1, variable2)
            #print('Number of values:', values_before)
            
            # CHeck for improvements
            values_after = 0
            for variable in self.domains:
                values_after += len(self.domains[variable])
            
            if values_before == values_after:
                break
        
        # Test whether any variable domain is empty
        for variable in self.domains:
            if self.domains[variable] == set():
                return False
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(self.domains) == len(assignment):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Initiate check variable
        check = True
        
        # 1. Check for distinct words
        distinct = set()
        for variable in assignment:
            distinct.add(assignment[variable])
        if len(assignment) != len(distinct):
            check = False

        # 2. Check for word length
        for variable in assignment:
            if len(assignment[variable]) != variable.length:
                check = False

        # 3. Check for conflicts
        for variable1 in assignment:
            for variable2 in assignment:
                if variable1 != variable2:
                    overlap = self.crossword.overlaps[variable1, variable2]
                    if overlap != None:
                        if assignment[variable1][overlap[0]] != assignment[variable2][overlap[1]]:
                            check = False

        # Return check variable
        return check

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Initiate word list for variables without neighbors
        word_list = list(self.domains[var])
        
        # Sort list for variable with neighbors
        if self.crossword.neighbors(var) != set():
            values = []
            for variable in self.crossword.neighbors(var):
                if variable in assignment:
                    continue
                overlap = self.crossword.overlaps[var, variable]
                for word1 in self.domains[var]:
                    value = 0
                    for word2 in self.domains[variable]:
                        if word1[overlap[0]] == word2[overlap[1]]:
                            value +=1
                    values.append(value)
                word_list = [x for _, x in sorted(zip(values,self.domains[var]), key=lambda pair: pair[0], reverse = True)]
        
        # Return word list
        return word_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Compute set of unassigned variables
        unassigned_variables = []
        for variable in self.domains:
            if variable not in assignment:
                unassigned_variables.append(variable)

        # 1. Select variables with fewest values
        values = []
        for variable in unassigned_variables:
            values.append(len(self.domains[variable]))        
        unassigned_variables = [x for _, x in sorted(zip(values,unassigned_variables), key=lambda pair: pair[0])]
        number_variables = 0
        for value in values:
            if value == min(values):
                number_variables += 1
        unassigned_variables = unassigned_variables[:number_variables]
        
        # 2. Select variable with lowest degree
        values = []
        for variable in unassigned_variables:
            values.append(len(self.crossword.neighbors(variable)))
        unassigned_variable = unassigned_variables[values.index(max(values))]

        # Return variable
        return unassigned_variable
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Create set with assigned variables
        assignment = dict()
        for variable in self.domains:
            if len(self.domains[variable]) == 1:
                assignment[variable] = list(self.domains[variable])[0]
        #print('\nFirst Assignment:', assignment)
        
        # Optimize word choice
        while True:
            
            # Stop rule when assignment complete
            if self.assignment_complete(assignment):
                return assignment
            else:
                variable = self.select_unassigned_variable(assignment)
                values = self.order_domain_values(variable, assignment)
                for value in values:
                    assignment[variable] = value
                    if self.consistent(assignment):
                        break
                #print('\nNew assignment:', assignment)


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
