
class Vendor:

    def __init__(self, inventory=None):
        self.inventory = inventory if inventory else []
    
    def add(self, item):
        """
        add an item to the inventory
        return added item
        """
        if item:
            self.inventory.append(item)
        return item
    
    def remove(self, item):
        """
        remove an item from inventory
        return removed item or None if not found
        """
        removed = item
        if item in self.inventory:
            self.inventory.remove(item)
        else:
            removed = None
        return removed
    
    def get_by_id(self, id):
        """
        find if item of an given id exist in inventory
        return found item or None
        """
        found = None
        for item in self.inventory:
            if item.id == id:
                found = item
        return found

    def swap_items(self, other_vendor, my_item, their_item):
        """
        swap given items between my inventory and other vendor
        return True if targeted items exist and swapped, False otherwise
        """
        swapped = False
        found_mine = None if my_item is None else self.get_by_id(my_item.id)
        found_theirs = None if their_item is None else other_vendor.get_by_id(their_item.id)
        if found_mine is not None and found_theirs is not None:
            other_vendor.add(self.remove(my_item))
            self.add(other_vendor.remove(their_item))
            swapped = True
        return swapped
    
    def swap_first_item(self, other_vendor):
        """
        swap first item of inventory from self and other vendor
        return True if both inventories are not empty and swapped, False otherwise
        """
        swapped = False
        if self.inventory and other_vendor.inventory:
            other_vendor.add(self.remove(self.inventory[0]))
            self.add(other_vendor.remove(other_vendor.inventory[0]))
            swapped = True
        return swapped
    
    def get_by_category(self, category):
        """
        return a list of item from inventory of given category
        return empty list if no item in the inventory is of the give category
        """
        items = list()
        for item in self.inventory:
            if item.get_category() == category:
                items.append(item)
        return items
    
    def get_best_by_category(self, category):
        # I was thinking implement it with only lambda function, but couldn't figure out how to :/
        """
        return None if inventory is empty or no such category DNE in the inventory
        else return the first best conditioned item of the category
        """
        items = self.get_by_category(category)
        item = None if not items else max(items, key=lambda i: i.condition)
        return item
    
    def swap_best_by_category(self, other_vendor, my_priority, their_priority):
        """
        find best conditioned item of given category of each person (self vendor, other vendor)
        if desired items are in eachother's inventory, swap them
        if any items not exist or inventory empty, return None
        """
        i_have = self.get_best_by_category(their_priority)
        vendor_has = other_vendor.get_best_by_category(my_priority)
        return self.swap_items(other_vendor, i_have, vendor_has)
    
    def display_inventory(self, category=None):
        """
        print all inventory of some inventory of a given category
        print a message if inventory is empty or no inventory of the given category
        """
        items = self.inventory if category is None else self.get_by_category(category)
        result = str()
        if items:
            for ind, item in enumerate(items):
                # this part took me (and Sam) forever to figure out :/
                # and Monica told me she prints out line by line so never encountered such problem
                result += '{}. {}'.format(ind+1, item.__str__())
                result += '\n' if ind+1 < len(items) else ''
        else:
            result = "No inventory to display."
        print(result)

    def swap_by_id(self, other_vendor, my_item_id, their_item_id):
        """
        use my_item_id and their_item_id to find the corresponding items
        return True if two items swapped successfully, False otherwise
        """
        my_item = self.get_by_id(my_item_id)
        their_item = other_vendor.get_by_id(their_item_id)
        return self.swap_items(other_vendor, my_item, their_item)

    def choose_and_swap_items(self, other_vendor, category=""):
        """
        let user choose items the swap the choosen items
        return True if swap succeed, False otherwise
        """
        # list inventory
        self.display_inventory(category)
        other_vendor.display_inventory(category)
        # promp user for input
        self_id = int(input("Please enter the id number of the item from your own inventory: "))
        other_id = int(input("Please enter the id number of the item from the other vendor's inventory: "))
        # swap the two items
        return self.swap_by_id(other_vendor, self_id, other_id)
    
    def get_item_feature(self, item):
        """
        return the feature the item has
        """
        category = item.__str__()
        # in operator is not very efficient here
        # but i cannot think of a better and simpler way
        if "Clothing" in category:
            feature = item.fabric
        elif "Decor" in category:
            feature = item.width * item.length
        elif "Electronics" in category:
            feature = item.type
        else:
            feature = None
        return feature
        
    
    def swap_similar_with_other_vendor(self, other_vendor, item):
        """
        if vendor has item similar to item I want to swap, swap it
        else return None
        """
        feature = self.get_item_feature(item)
        swapped = False
        for vendor_item in other_vendor.inventory:
            if feature and other_vendor.get_item_feature(vendor_item) == feature:
                swapped = self.swap_items(other_vendor, item, vendor_item)
                break
        return swapped
