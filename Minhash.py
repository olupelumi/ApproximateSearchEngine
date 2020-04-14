#necessary imports
from sklearn.utils import murmurhash3_32
import random
from collections import defaultdict

#Setting my seed so my results are reproducible
random.seed(1)

def MinHash(stg, sd):
    '''
    Inputs a string stg and a seed
    Returns the minimum hash value using the 3-gram representation of the strings
    '''
    
    #Converting the stg into a set of 3-grams
    slen = len(stg)
    three_gram_lst = [stg[i:i+3] for i in range(slen-2)]    
    #hashes each 3-gram and returns the minhash value
    return min([murmurhash3_32(strg,seed = sd) for strg in three_gram_lst])


#Design of this still in process
#Definitely need multiple hashmaps.
class HashTable():
    def __init__(self, K, L, B, R):
        self.K = K #number of hash functions
        self.L = L #number of hash tables
        self.B = B #number of buckets in the hash table
        self.R = R #range of the hash functions
        
        #L hashmaps(dictionaries) that will map strings to arrays(buckets)
        self.L_lst = [defaultdict(set) for l in range(self.L)]
        
        #Creating the seeds for my each of the k*L hash functions
        self.h_sd_arr = [[random.randrange(self.K * self.L * 2) for i in range(self.K)] for j in range(self.L)]
        #self.id = 0
    def insert(self,s_input, idee):
        '''
        Input a string s and an integer id that coincides with it. 
        Returns nothing
        adds the id to each of the L hashtables after minhashing each k times to get the proper bucket
        '''
       
        
        #Number used to know which vector of seeds
        cnt = 0  
        for htable in self.L_lst:
            #Need to figure out how to use all the seeds I created(just use the indexes probably)
            key_str = "" #string that I will hash later
            
            #Hash the string k times and turn the hash values to strings, concatenate them and put them in a mapping  of some sort
            for k_hash_seed in self.h_sd_arr[cnt]:
                kstring = str(MinHash(s_input, k_hash_seed) % self.R)
                key_str += kstring
                
            #Now I need to add the id into the bucket of the hashtable
            htable[key_str].add(idee)
            cnt +=1
    def lookup(self, query):
        '''
        Inputs a string query query
        Returns a set of all the unique ids that are similar. These ids can be later mapped to strings
        '''
        similar_set = set([])
        cnt = 0
        for h_table in self.L_lst:
            #hash the query k times and get the corresponding string
            key_str = "" #string that I will use as a key to a bucket
            
            for k_hash_seed in self.h_sd_arr[cnt]:
                kstring = str(MinHash(query, k_hash_seed) % self.R)
                key_str += kstring           
                
            #find the bucket of each set and do a union with the similar_set
            curr_set = h_table[key_str]
            similar_set = similar_set.union(curr_set)
            
            cnt += 1 #chanhing to the next vector of seeds for hashing
            
        return similar_set