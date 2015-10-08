import os.path
import sys
from collections import deque

class Graph:

    def __init__(self, v):
        self.__V = v
        self.__Adj = []
        for i in range(v):
            self.__Adj.append(set())
        self.__E = 0

    def v(self):
        return self.__V

    def e(self):
        return self.__E

    def add_edge(self, v, w):
        self.__Adj[v].add(w)
        self.__Adj[w].add(v)
        self.__E += 1

    def adj(self, v):
        return self.__Adj[v]

    def degree(self, v):
        result=0
        for w in self.__Adj(v):
            result+=1
        return result

    def maxDegree(self):
        result=0
        for v in range(self.v()):
            aux=self.degree(v)
            if (aux > result):
                result=aux
        return result

    def avgDegree(self):
        return 2*self.g()/self.v()

    def numberOfSelfLoops(self):
        result=0
        for v in range(self.v()):
            for w in self.__Adj(v):
                if (v == w):
                    result += 1
        result=result / 2
        return result

class DepthFirstPaths:
    def __init__(self, g, s):
        self.__Marked = [ False for i in range(g.v()) ]
        self.__EdgeTo = [ - 1 for i in range(g.v()) ]
        self.__S = s
        self.__dfs(g, s)

    def __dfs(self, g, v):
        self.__Marked[v] = True
        for w in g.adj(v):
            if not self.__Marked[w]:
                self.__EdgeTo[w] = v
                self.__dfs(g, w)

    def has_path_to(self, v):
        return self.__Marked[v]

    def path_to(self, v):
        result=None
        if self.has_path_to(v):
            result = []
            x=v
            while x != self.__S:
                result.append(x)
                x = self.__EdgeTo[x]
            result.append(self.__S)
        return result[::-1]

class BreadthFirstPaths:
    def __init__(self, g, s):
        self.__Marked = [ False for i in range(g.v()) ]
        self.__EdgeTo = [ - 1 for i in range(g.v()) ]
        self.__S = s
        self.__bfs(g, s)

    def __bfs(self, g, s):
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
        return self.__Marked[v]

    def path_to(self, v):
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
                self.__Words = self._read_lines_from_file(wordfile)
                if len(self.__Words) == 0:
                    raise ValueError("%s is empty" % wordfile)
            else:
                raise ValueError("%s does not exist" % wordfile)
        
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

    def __find_intermediates_recursively(self, origin, destination, wordlist, inprocess=[]):
        result=[]
        candidates=self._those_at_distance(origin, [ node for node in wordlist if node not in inprocess ], 1)
        for candidate in candidates:
            if candidate == destination:
                result.append(candidate)
                break
            else:
                inprocess.append(candidate)
                aux=self.__find_intermediates_recursively(candidate, destination, wordlist, inprocess)
                if len(aux) > 0:
                    result=list(inprocess)
                    break
                else:
                    inprocess.remove(candidate)
        return result

    def find_word_path(self, origin, destination):
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
    
def main(argv):
    if len(argv) != 4:
        raise ValueError("Usage: wordpaths.py wordfile startword endword")
    print_path(Wordpath(argv[1]).find_word_path(argv[2], argv[3]))

if __name__ == "__main__":
    main(sys.argv)
