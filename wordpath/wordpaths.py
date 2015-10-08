import os.path
import sys
from collections import deque

class Graph:
    """
    A graph implemented as a data structure
    consisting of an array containing the list
    of adjacents to the vertice associated to
    that array index.

    Consider this graph.
                         +--+    +--+
                         |6 <----|5 |
                         +--+   >+--+
                               /   ^
                              /    |
                +--+     +--+/    ++-+
                |1 |<----+0 +---->|4 |
                +--+     ++-+\    ++-+
                    \     |   \    ^
                     \    v    \   |
                      \ +--+    >+-++
                       >|2 |     |3 |
                        +--+     +--+






   vertice           Adjacents
               +--------------------------+
    +--+       | +--+ +--+ +--+ +--+ +--+ |
    |0-+------>| |1 | |2 | |3 | |4 | |5 | |
    +--+       | +--+ +--+ +--+ +--+ +--+ |
               +--------------------------+
               +------+
    +--+       | +--+ |
    |1-+------>| |2 | |
    +--+       | +--+ |
               +------+
               +--+
    +--+       |  |
    |2-+------>|  |
    +--+       |  |
               +--+
               +------+
    +--+       | +--+ |
    |3-+------>| |4 | |
    +--+       | +--+ |
               +------+
               +------+
    +--+       | +--+ |
    |4-+------>| |5 | |
    +--+       | +--+ |
               +------+
               +------+
    +--+       | +--+ |
    |5-+------>| |6 | |
    +--+       | +--+ |
               +------+
               +--+
    +--+       |  |
    |6-+------>|  |
    +--+       |  |
               +--+

    The information about the graph is expected
    to be provided by calling
    graph.add_edge(vertice, neighbour).
    """
    def __init__(self, v):
        """
        Initializes the graph structureo
        """
        self.__V = v
        self.__Adj = []
        for i in range(v):
            self.__Adj.append(set())
        self.__E = 0

    def v(self):
        """
        Retrieves the number of vertices.
        """
        return self.__V

    def e(self):
        """
        Retrieves the number of edges.
        """
        return self.__E

    def add_edge(self, v, w):
        """
        Adds a new edge to the graph: a direct
        connection between two vertices.
        """
        self.__Adj[v].add(w)
        self.__Adj[w].add(v)
        self.__E += 1

    def adj(self, v):
        """
        Retrieves the adjacents of a given vertice.
        """
        return self.__Adj[v]

class BreadthFirstPaths:
    """
    Algorithm to traverse a graph using a breadth-first
    approach. It guarantees it finds the shortest path
    between two connected vertices.
    Notice that a depth-first approach is limited by
    the stack size since it's recursive by definition.
    """
    def __init__(self, g, s):
        """
        Initializes the internal structure.
        """
        self.__Marked = [ False for i in range(g.v()) ]
        self.__EdgeTo = [ - 1 for i in range(g.v()) ]
        self.__S = s
        self.__bfs(g, s)

    def __bfs(self, g, s):
        """
        Traverses the graph using a FIFO, exhaustively
        visiting each vertice at the same depth.
        It keeps track of whether it has already visited
        a vertice in the __Marked array, and annotates
        the parent for each node in __EdgeTo.
        """
        queue=deque()
        self.__Marked[s] = True
        queue.append(s)
        while not len(queue) == 0:
            v = queue.popleft()
            for w in g.adj(v):
                if not self.__Marked[w]:
                    self.__EdgeTo[w] = v
                    self.__Marked[w] = True
                    queue.append(w)

    def has_path_to(self, v):
        """
        Checks whether there's a path
        from the source vertice to a given node.
        """
        return self.__Marked[v]

    def path_to(self, v):
        """
        Retrieves the path from the source to given vertice,
        if it exists.
        The process is:
        - Starting with the destination,
          use __EdgeTo structure iteratively to find the parent,
          annotating them,
          until it reaches the top (source).
        - Then, reverse the parent vertices found in the process.
        """
        result=None
        if self.has_path_to(v):
            result = []
            x=v
            while x != self.__S:
                result.append(x)
                x = self.__EdgeTo[x]
            result.append(self.__S)
        return result[::-1]


class Wordpath:
    def __init__(self, wordfile, withintest=False):
        r"""
        Constructs a new instance.
        >>> w=Wordpath("/usr/share/dict/words")

        >>> w=Wordpath("/tmp/nothing")
        Traceback (most recent call last):
        ValueError: /tmp/nothing does not exist

        To test for empty files, execute this on a shell:
        $ touch /tmp/empty
        >>> w=Wordpath("/tmp/empty")
        Traceback (most recent call last):
        ValueError: /tmp/empty is empty
        """
        if not withintest:
            if self._file_exists(wordfile):
                self.set_words(self._read_lines_from_file(wordfile))
                if len(self.__Words) == 0:
                    raise ValueError("%s is empty" % wordfile)
            else:
                raise ValueError("%s does not exist" % wordfile)

    def set_words(self, newList):
        self.__Words = newList

    def _file_exists(self, filepath):
        r"""
        Checks whether the file exists.
        >>> Wordpath(None, True)._file_exists("/usr/share/dict/words")
        True
        >>> Wordpath(None, True)._file_exists("/tmp/nothing.txt")
        False
        """
        return os.path.isfile(filepath)

    def _read_lines_from_file(self, filepath):
        r"""
        Reads a file one line at a time, and stores them in an array.
        $ echo "first" > /tmp/test.txt; echo "second" > /tmp/test2.txt
        >>> Wordpath(None, True)._read_lines_from_file("/tmp/test2.txt")
        ['first', 'second']
        """
        f = open(filepath)
        result = [ w.strip() for w in f.readlines() ]
        f.close()
        return result

    def _hamming_distance(self, first, second):
        r"""
        Calculates the hamming distance between both words.
        Implementation taken from wikipedia: https://en.wikipedia.org/wiki/Hamming_distance
        >>> Wordpath(None, True)._hamming_distance("abc", "bbc")
        1
        >>> Wordpath(None, True)._hamming_distance("abc", "bbb")
        2
        >>> Wordpath(None, True)._hamming_distance("aabbcc", "bbbbca")
        3
        >>> Wordpath(None, True)._hamming_distance("abc", "aabbcc")
        Traceback (most recent call last):
        ValueError: Undefined for sequences of unequal length (abc - aabbcc)
        >>> Wordpath(None, True)._hamming_distance("rial", "rain")
        3
        """
        if len(first) != len(second):
            raise ValueError("Undefined for sequences of unequal length (%s - %s)" % (first, second))
        return sum(ch1 != ch2 for ch1, ch2 in zip(first, second))

    def _those_at_distance(self, word, wordlist, distance):
        r"""
        Filters given word list, selecting only those matching their
        hamming distance is the one given.
        >>> words=["real","rain","coal","feal","foal","foul","foud","fear","fast","loud"]
        >>> Wordpath(None, True)._those_at_distance("rial", words, 1)
        ['real']
        >>> Wordpath(None, True)._those_at_distance("rial", words, 2)
        ['coal', 'feal', 'foal']
        >>> Wordpath(None, True)._those_at_distance("rial", words, 3)
        ['rain', 'foul', 'fear']
        >>> Wordpath(None, True)._those_at_distance("rial", words, 4)
        ['foud', 'fast', 'loud']
        """
        return [ w for w in wordlist if word != w and len(word) == len(w) and self._hamming_distance(word, w) == distance ]

    def find_word_path(self, origin, destination):
        r"""
        Finds the words from the list which, in sequence,
        transforms the origin into the destination by
        changing a single character each time (Hamming distance 1).
        >>> words=["rial", "real", "feal", "foal", "foul", "foud", "dung", "dunt", "dent", "gent", "geet", "geez", "jehu", "jesu", "jest", "gest", "gent", "gena", "guna", "guha", "yagi", "yali", "pali", "palp", "paup", "plup", "blup", "bitt", "butt", "burt", "bert", "berm", "berm", "germ", "geum", "meum", "jina", "pina", "pint", "pent", "peat", "prat", "pray", "fike", "fire", "fare", "care", "carp", "camp" ]
        >>> wordpath=Wordpath(None, True)
        >>> wordpath.set_words(words)
        >>> wordpath.find_word_path("rial", "foud")
        Building graph ... done
        Initializing search algorithm ... done
        ['rial', 'real', 'feal', 'foal', 'foul', 'foud']
        >>> wordpath.find_word_path("dung", "geez")
        Building graph ... done
        Initializing search algorithm ... done
        ['dung', 'dunt', 'dent', 'gent', 'geet', 'geez']
        >>> wordpath.find_word_path("jehu", "guha")
        Building graph ... done
        Initializing search algorithm ... done
        ['jehu', 'jesu', 'jest', 'gest', 'gent', 'gena', 'guna', 'guha']
        >>> wordpath.find_word_path("yagi", "blup")
        Building graph ... done
        Initializing search algorithm ... done
        ['yagi', 'yali', 'pali', 'palp', 'paup', 'plup', 'blup']
        >>> wordpath.find_word_path("bitt", "meum")
        Building graph ... done
        Initializing search algorithm ... done
        ['bitt', 'butt', 'burt', 'bert', 'berm', 'germ', 'geum', 'meum']
        >>> wordpath.find_word_path("jina", "pray")
        Building graph ... done
        Initializing search algorithm ... done
        ['jina', 'pina', 'pint', 'pent', 'peat', 'prat', 'pray']
        >>> wordpath.find_word_path("fike", "camp")
        Building graph ... done
        Initializing search algorithm ... done
        ['fike', 'fire', 'fare', 'care', 'carp', 'camp']
        """
        lst=[]
        indexes={}
        i=0
        subset=[ word for word in self.__Words if len(word) == len(origin) ]
        count=len(subset)
        graph=Graph(count)
        for w in subset:
            indexes[w]=i
            lst.append(w)
            i+=1
        i=0
        print("Building graph ... ", end="")
        sys.stdout.flush()
        for w in subset:
            i+=1
            for close_match in self._those_at_distance(w, subset, 1):
                graph.add_edge(indexes[w], indexes[close_match])
        print("done")
        sys.stdout.flush()
        print("Initializing search algorithm ... ", end="")
        searchAlgorithm=BreadthFirstPaths(graph, indexes[origin])
        print("done")
        sys.stdout.flush()
        path=searchAlgorithm.path_to(indexes[destination])
        if path == None:
            print("No path from %s to %s" % (origin, destination))
            result = None
        else:
            result=[ lst[i] for i in path ]

        return result

def print_path(wordpath):
    r"""
    Prints a word path using -> as separators.
    >>> wordpath=["butt", "burt", "bert", "berm", "germ", "geum"]
    >>> print_path(wordpath)
    butt -> burt -> bert -> berm -> germ -> geum
    """
    print(" -> ".join(wordpath))

def usage():
    result=""""
Error: Invalid input: Too few or too many arguments.

Usage: wordpaths.py wordfile startword endword
Where:
  - wordfile: a file with a list of words, one per line.
  - startword: the word to start with.
  - endword: the word to end with.
"""
    return result

def main(argv):
    if len(argv) != 4:
        raise ValueError(usage())
    print_path(Wordpath(argv[1]).find_word_path(argv[2], argv[3]))

if __name__ == "__main__":
    main(sys.argv)
