# Lecture 17 - 31OCT22
##### Demo: counting tree nodes
```java
if (tree == null) {
	return 0;
}
return 1 + count(tree.left) + count(tree.right)
```

#### Complexity of tree traversal
Traversing all nodes will take **O(N)** time, if perfectly balanced
Traversing is more precisely: 
$$2T(\frac{N}{2})+O(1)$$
Provided table of common recursion relation/Big-O will translate recursion relation to asymptotic runtime.

A perfectly imbalanced binary search tree is effectively a linked list.

#### Should we worry about balance?
No:
- adding values randomly, your binary search tree will look roughly balanced and perform as such

Yes:
- not confident that nodes will be added in truly random order

#### How much balance is enough?
To get ideal asymptotic performance, we only have to be *approximately* balanced.

**Approximate balance**: every node rooting a subtree of size $n \ge a$, the left and right subtrees of the node both contain at most $b(\frac{n}{2})$ nodes.

The better the balance factor, the better the complexity, but not a huge deal when judging approximate runtime complexity.

