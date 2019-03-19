class BinaryTree:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

    def left(self):
        return self.left

    def right(self):
        return self.right

    def value(self):
        return self.value

    def is_leaf(self):
        return self.left is None and self.right is None

    def size(self):
        cur_size = 1
        if self.left is not None:
           cur_size += self.left.size()
        if self.right is not None:
            cur_size += self.right.size()
        return cur_size

class MRP:

    def construct_tree(self, data, cur_index = 0):
        cur_root = BinaryTree(data[cur_index][2])
        left_tree_index = cur_index + 1
        if left_tree_index < len(data) and int(data[left_tree_index][0]) > int(data[cur_index][0]):
            cur_root.left = self.construct_tree(data, left_tree_index)

        right_tree_index = cur_index + 1
        if cur_root.left is not None:
            right_tree_index += cur_root.left.size()
        if right_tree_index < len(data) and int(data[right_tree_index][0]) > int(data[cur_index][0]):
            cur_root.right = self.construct_tree(data, cur_index + 1 + cur_root.left.size())
        return cur_root

    def traverse_tree(self, root):
        if root is None:
            return

        print (root.value)
        self.traverse_tree(root.left)
        self.traverse_tree(root.right)

    def read_tree(self, file_name):
        file = open(file_name, "r")
        data = file.readlines()
        parsed = []
        for line in data:
            split = line.split(',')
            split[2] = split[2].replace('\n', '')
            parsed.append(split)

        return self.construct_tree(parsed)

    def read_parts(self, file_name):
        file = open(file_name, "r")
        data = file.readlines()
        dict = {}
        for line in data:
            split = line.split(',')
            # saves count, price
            dict[split[0]] = [int(split[2]), int(split[3])]
        return dict

    def read_subassemblies(self, file_name):
        file = open(file_name, "r")
        data = file.readlines()
        dict = {}
        for line in data:
            split = line.split(',')
            dict[split[0]] = int(split[1])
        dict['coolbike'] = 0
        dict['boringbike'] = 0
        return dict

    def __init__(self, cool_file, boring_file, parts_file, subassemblies_file):
        self.cool_tree = self.read_tree(cool_file)
        self.boring_tree = self.read_tree(boring_file)
        self.parts_data = self.read_parts(parts_file)
        self.subassemblies_data = self.read_subassemblies(subassemblies_file)

    def calc_verify(self, tree, quantity):
        if tree.is_leaf():
            if self.parts_data[tree.value][0] >= quantity:
                return True
            else:
                return False
        else:
            if self.subassemblies_data[tree.value] >= quantity:
                return True
            else:
                return self.calc_verify(tree.left, quantity - self.subassemblies_data[tree.value]) and \
                       self.calc_verify(tree.right, quantity - self.subassemblies_data[tree.value])

    def procurement(self, tree, quantity):
        if tree.is_leaf():
            if self.parts_data[tree.value][0] < quantity:
                needed_amount = quantity - self.parts_data[tree.value][0]
                buy_amount = needed_amount
                if needed_amount >= 7:
                    buy_amount += 2
                else:
                    buy_amount += 1
                self.parts_data[tree.value][0] += buy_amount
        else:
            self.procurement(tree.left, quantity)
            self.procurement(tree.right, quantity)


    def exec_order(self, tree, quantity):
        if tree.is_leaf():
            self.parts_data[tree.value][0] -= quantity
        else:
            if self.subassemblies_data[tree.value] >= quantity:
                self.subassemblies_data[tree.value] -= quantity
            else:
                self.exec_order(tree.left, quantity - self.subassemblies_data[tree.value])
                self.exec_order(tree.right, quantity - self.subassemblies_data[tree.value])
                self.subassemblies_data[tree.value]  = 0

    def after_order(self, tree, quantity):
        if tree.is_leaf():
            return
        else:
            if quantity <= 5:
                self.subassemblies_data[tree.value] += 1
            else:
                self.subassemblies_data[tree.value] += int(round(quantity / 3))
            self.after_order(tree.left, quantity)
            self.after_order(tree.right, quantity)

    def clientInput(self, product_name, quantity):
        cur_tree = self.cool_tree
        if product_name == 'BoringTree':
            cur_tree = self.boring_tree

        if self.calc_verify(cur_tree, quantity):
            self.exec_order(cur_tree, quantity)
        else:
            self.procurement(cur_tree, quantity)
            self.exec_order(cur_tree, quantity)
        self.after_order(cur_tree, quantity)

    def show_parts(self):
        print('PARTS')
        for key in self.parts_data:
            print(key, ' --- ', self.parts_data[key])

    def show_subassemblies(self):
        print('SUBASSEMBLIES')
        for key in self.subassemblies_data:
            if key != 'coolbike' and key != 'boringbike':
                print(key, ' --- ', self.subassemblies_data[key])


if __name__ == '__main__':
    
    mrp = MRP('coolbike.dat', 'boringbike.dat', 'parts.dat', 'subassemblies.dat')
    mrp.clientInput('BoringBike', 10)
    mrp.show_parts()
    mrp.show_subassemblies()
