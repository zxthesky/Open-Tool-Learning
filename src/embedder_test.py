import sys
sys.dont_write_bytecode = True

from otl.embedding import Embedder

if __name__ == "__main__":
    embedder = Embedder("D:\PTM\gte-base-en-v1.5")
    # output_vector = embedder(["txt1231241","aldklsalng"])
    output_vector = embedder("txt1231241")
    print(len(output_vector))
    print(output_vector[0].shape)
    # print(output_vector[1].shape)
