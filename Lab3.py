#CS2302
#Aaron Brown
#Diego Aguirre
#Anindita Nath
#11/4/18
#Read words and their embeddings from a file then store them in either an AVL or Red-Black Tree using the words as the keys then display the similarity of words
from AVLTree import AVLTree, Node
from RedBlackTree import RedBlackTree , RBTNode
import math

def main():
    tree = createTree()
    
    nodes = numberOfNodes(tree.root)
    print('Nodes:' + str(nodes))
    
    h = height(tree.root)
    print('Height:' + str(h))
    
    list = wordsInTreeInorder(tree.root)
    print('words in ascending order stored in words-inorder.txt')
    
    depth = 0
    keys = keysAtDepth(tree.root, depth)
    print('words at depth ' + str(depth) + ' stored in keys at depth ' + str(depth) + '.txt')

    printTree(tree.root)
    #wordList(list)
    #findSim2PerLine(tree)

 
def findSim2PerLine(tree): #read words from a file containing two words on each line then displays their similarity
    f = open('2wordsperline.txt')
    
    for words in f:
        i=0
        while i < len(words) and words[i] != ' ':
            i+=1
        word1 = words[0:i]
        word2 = words[i+1:-1]
        
        if word2 == '':
            print(word1 ,end = ', ')
            print('only one word on line')
        else:
            sim = findSim(word1 ,word2 ,tree)
            print('Similarity between (' + word1 + ','+ word2 +'):' + str(sim))
    
def createTree(): #creates either an AVL Tree or Red-Black Tree and stores words as the keys
    tree_type = -1
    word_embeddings = open('glove.6B.50d.txt')
    
    while tree_type != '1' and tree_type != '2':
        print("Use AVL Tree or Red-Black Tree?")
        print("Type 1 for AVL")
        print("Type 2 for Red-Black")
        tree_type = input()
        
    if tree_type == '1':
        tree = AVLTree()
        #for i in range(50): #stores first 50 words
        for word in word_embeddings: #stores all words in list
            #word = word_embeddings.readline()
            if word[0].isalpha() == True: #ignores words that do not start with an alphabetic character
                node = Node(getWord(word) , getWordEmbedding(word))
                tree.insert(node)
        word_embeddings.close()
        return tree
    
    if tree_type == '2':
        tree = RedBlackTree()
        #for i in range(50): #stores first 50 words
        for word in word_embeddings: #stores all words in list
            #word = word_embeddings.readline()
            if word[0].isalpha() == True:
                tree.insert(getWord(word) ,getWordEmbedding(word))
        word_embeddings.close()
        return tree
     
def printTree(root): #prints tree inorder
    if root != None:
        printTree(root.left)
        print(root.key)        
        printTree(root.right)
        
def numberOfNodes(root):#return number of nodes in the tree
    if root == None:
        return 0
    nodes = 1
    nodes += numberOfNodes(root.left)
    nodes += numberOfNodes(root.right)
    return nodes    

def height(root):#returns the height of the tree
    if root == None:
        return -1
    left_height = height(root.left)
    right_height = height(root.right)
    return max(left_height , right_height) + 1

def keysAtDepth(root , d):#Generates a file with all keys at depth d in ascending order
    words = open('keys at depth ' + str(d) + '.txt' , 'w')
    keysAtDepthHelper(root, words , d)
    words.close()

def keysAtDepthHelper(root, words , d):#keysAtDepth helper method
    if root == None:
        return
    if d == 0:
        words.write(root.key + '\n')
    keysAtDepthHelper(root.left , words , d-1)
    keysAtDepthHelper(root.right , words , d-1)
    
def wordsInTreeInorder(root):#Generates a file containing all words in tree in ascending order one per line and returns a list of words
    wordsInorder = open('words-inorder.txt' , 'w')
    list = wordsInTreeInorderHelper(root , wordsInorder)
    wordsInorder.close()
    return list
    
def wordsInTreeInorderHelper(root , wordsInorder):#helper method for wordsInTree
    if root == None:
        return
    list = []
    if root.left != None:
        list += wordsInTreeInorderHelper(root.left , wordsInorder)
    wordsInorder.write(root.key +'\n')
    list.append(root.key)
    if root.right != None:
        list += wordsInTreeInorderHelper(root.right , wordsInorder)
    return list
 
def findSim(w0 ,w1 ,tree): #returns similarity of two words
    e0 = tree.search(w0).embedding
    e1 = tree.search(w1).embedding 

    similarity = dotProduct(e0,e1) / ( magnitude(e0) * magnitude(e1) )
    
    return similarity
    
def dotProduct(e0 , e1): #returns dot product of two embeddings
    sum = 0
    for i in range(len(e0)):
        sum += e0[i] * e1[i]
    return sum

def magnitude(e): #returns magnitude of embedding
    sum = 0
    for i in range(len(e)):
        sum += e[i] ** 2
    return math.sqrt(sum)

def getWord(word): #returns word without embedding
    i = 0
    while word[i].isspace() != True:
        i+=1
    return word[0:i]

def getWordEmbedding(word):#returns word embedding without word
    i = 0
    while word[i].isspace() != True: 
        i+=1
    i+=1
    
    e = []
    while  i < len(word):
        j = i
        if word[i].isnumeric() or word[i] == '-':
            while j < len(word) and word[j].isspace() == False:
                j += 1
            e.append(float(word[i:j]))
        i = j + 1
        
    return e

def wordList(words):# writes a file with two words in each line
    f = open('2wordsperline.txt' ,'w')
    for i in range(len(words)):
        f.write(words[i])
        if i % 2 == 1:
            f.write('\n')
        else:
            f.write(' ')
    f.close()
    

main()
