"""
#####Summarize all kind of ways to do Tree Traversal
* BFS
  * Level Order Traversal(Use double loop)
* DFS
  * Preorder(Recursive, Iterative)
  * Inorder(Recursive, Iterative)
  * Postorder(Recursive, Iterative)
"""

from Tree_Helper.tree_helper import *

def BFS_level_order_traversal(root):
    if not root:
        return
    queue = [root]
    ret = []
    while len(queue) > 0:
        size = len(queue)
        level = []
        for i in range(size):
            node = queue.pop()
            level.append(node.val)
            if node.left:
                queue.insert(0, node.left)
            if node.right:
                queue.insert(0, node.right)
        ret.append(level[:])
    return ret


def DFS_level_order_traversal(root):
    ret = {}
    DFS_helper(ret, 1, root)
    for level in sorted(ret.keys()):
        print ret[level]

def DFS_helper(ret, level, root):
    if not root:
        return

    ret.setdefault(level, []).append(root.val)
    DFS_helper(ret, level + 1, root.left)
    DFS_helper(ret, level + 1, root.right)


# Recursive Ways
def DFS_preorder(root):
    if not root:
        return
    print root.val
    DFS_preorder(root.left)
    DFS_preorder(root.right)

def DFS_inorder(root):
    if not root:
        return
    DFS_inorder(root.left)
    print root.val
    DFS_inorder(root.right)

def DFS_postorder(root):
    if not root:
        return
    DFS_postorder(root.left)
    DFS_postorder(root.right)
    print root.val


# Iterative Ways

# push right first then left
def DFS_perorder(root):
    if not root:
        return
    stack = [root,]
    while len(stack) > 0:
        node = stack.pop()
        print node.val
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

# if no left, move to right
def DFS_inorder(root):
    if not root:
        return
    stack = []
    cur = root
    while True:
        while cur:
            stack.append(cur)
            cur = cur.left
        if not stack:
            break
        cur = stack.pop()
        print cur.val
        cur = cur.right

# reverse the reversed preorder
def DFS_postorder(root):
    if not root:
        return
    stack = [root,]
    ret = []
    while len(stack) > 0:
        node = stack.pop()
        ret.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    print ret[::-1]


# Divde and Conquer
def DFS_preorder(root):
    if not root:
        return []

    left  = DFS_preorder(root.left)
    right = DFS_preorder(root.right)

    result.append(root.val)
    result.extend(left)
    result.extend(right)
    return result

def DFS_postorder(root):
    if not root:
        return []

    left = DFS_postorder(root.left)
    right = DFS_postorder(root.right)

    result.extend(left)
    result.extend(right)
    result.append(root.val)             # ?WTF just switch the place?
    return result


A = [ i for i in range(10) ]
new_tree = create_bst_from_array(A)
"""
print new_tree.val

print BFS_level_order_traversal(new_tree)
print '-' * 10
DFS_level_order_traversal(new_tree)
print '-' * 10
DFS_inorder(new_tree)
DFS_preorder(new_tree)
DFS_postorder(new_tree)
"""

```
#### Flatten BST to (Doubly) linked list
1. Leetcode上面的原题是to single, 但是traversal是pre-order
2. 这里的doubly用的方法是in-order traversal, pre-order也是一样的思路
3. [网上](http://cslibrary.stanford.edu/109/TreeListRecursion.html)的题目还有点差别是要变成Circular Doubly Linked List
4. 稍微注意一下return的问题, 这两种recursion的方法都没有return值, 所以如果需要找head的话还得再处理下
5. 千万记得这里需要用到global declaration

#####Flatten思路
1. 最方便的方法还是用recursion
2. 先弄清需要的是preorder, inorder还是postorder的顺序
3. 选择对应order的traversal模板, 重要的一点是要把
   ```python
   left = root.left
   right = root.right
   ```
   提前存好，因为进行flatten之后可能会破坏树的结构，这步做好之后，XXXorder traversal的方法都是一样的了
4. 记得```global head, last```然后对```last```进行操作
   * Singly Linked List - 记得重置```last.left = None, last.right = root```
   * Doubly Linked List - 如果```last.right = root, root.left = last```
     这里有一点点差别就是如果是preorder的话，```head.left = None```需要单独处理下
5. ```last = root```更新```last```
6. ```head```就是初始设为None, 第一个需要处理的node就赋为```head```就行了

```python
#last = None
#head = None
def inorder_doubly_flatten(root):
    global last
    global head
    if not root:
        return
    inorder_doubly_flatten(root.left)
    if last:
        last.right = root
        root.left = last
    last = root
    if not head:                        # Used to get true HEAD
        head = root
    inorder_doubly_flatten(root.right)


#last = None
#head = None
def preorder_doubly_flatten(root):
    if not root:
        return
    global last
    global head
    right = root.right
    left = root.left
    if not head:
        head = last
    if last:
        last.right = root
        root.left = last
    else:
        root.left = None                # 小处理
    last = root

    preorder_doubly_flatten(left)
    preorder_doubly_flatten(right)

"""
print DFS_level_order_traversal(new_tree)

last = None
head = None
inorder_doubly_flatten(new_tree)
preorder_doubly_flatten(new_tree)

print BFS_level_order_traversal(new_tree)

print_tree_as_list(head)
"""
