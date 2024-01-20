import json
import collections
import os
import numpy as np

# Model Algorithms
# also tensor flow, there are multiple implementations of word2vec
from gensim.models import word2vec

# Visualisation
import matplotlib.pyplot as plt
import seaborn as sns


def read_data(file, filelist=[]):
    # Load the dataset
    # json format labels: brand, id number and fragrances (list)
    trainperfumes = json.load(open(file, 'r'))
    for f in filelist:
        trainperfumes.extend(json.load(open(f, 'r')))
    return trainperfumes


def quick_data_extraction(perfumes):
    raw_perfumes = list()
    for perfume in perfumes:
        raw_perfumes.append(perfume[u'perfume'].strip())

    raw_fragrances = list()
    for perfume in perfumes:
        for fragrance in perfume[u'fragrances']:
            raw_fragrances.append(fragrance.strip())

    raw_brands = list()
    for perfume in perfumes:
        raw_brands.append(perfume[u'brand'].strip())

    # use Counter to get frequencies
    counts_frag = collections.Counter(raw_fragrances)
    counts_perfume = collections.Counter(raw_perfumes)
    counts_brand = collections.Counter(raw_brands)

    # this will help us to have an idea how our corpora of fragrances looks like
    print('Size fragrances dataset (with repetition):  \t{}'.format((len(raw_fragrances))))
    print('Unique fragrances dataset: \t\t\t{}'.format((len(counts_frag.values()))))

    # This will provide a distribution of perfumes, indirect info of the fragrances
    print('Total # of perfumes \t\t\t\t{}'.format(len(counts_perfume)))
    print('Total # of brands \t\t\t\t{}'.format((len(counts_brand.values()))))

    # Dispersion of the frequencies fragrances
    print('Mean deviation of the fragrances frequencies:', end=' ')
    print(np.mean(list(counts_frag.values())))
    print('Standard deviation of the fragrances frequencies: ', end=' ')
    print(np.std(list(counts_frag.values())))

    # top 15
    print('\nTop 15 fragrances:')
    for f in counts_frag.most_common(15):
        print("\t {}".format(f))

    # Tail 15
    print('Tail 15 fragrances:')
    for f in counts_frag.most_common()[-15:]:
        print("\t {}".format(f))


def clean_data(perfumes):
    sentences = []
    # one hot fragrances

    for perfume in perfumes:
        clean_perfume = []
        # I want fragrance remove
        for fragrance in perfume['fragrances']:
            # minimal preprocessing
            fragrance = fragrance.lower().strip()
            clean_perfume.append(fragrance)
        sentences.append(clean_perfume)

    return sentences


def word_2_vec(sentences):
    # Set values for NN parameters
    num_features = 300  # Word vector dimensionality
    min_word_count = 1
    num_workers = 4  # Number of CPUs
    context = 10  # Context window size;
    downsampling = 1e-3  # threshold for configuring which higher-frequency words are randomly downsampled

    # Initialize and train the model
    model = word2vec.Word2Vec(sentences, workers=num_workers, min_count=min_word_count, window=context,
                              sample=downsampling, compute_loss=True)

    model.save('../word2vec.model')
    return model


def example(model):
    # print(len(model.wv.key_to_index))
    # print(model.wv.key_to_index)
    fragrance = 'rose'
    print("Most compatible with {}:".format(fragrance))
    # for frag, compatibility in model.wv.most_similar(u'feta cheese'):
    for frag, compatibility in model.wv.most_similar(positive=fragrance):
        print("\t\t -{}: {:.3f}".format(frag, compatibility))

    print('compatibility("red fruits", "water jasmine") = ', model.wv.similarity('red fruits', 'water jasmine'))


def main():
    model_filename = '../word2vec.model'
    if os.path.isfile(model_filename):
        model = word2vec.Word2Vec.load(model_filename)
        file = '../data/perfume_data.json'
        perfumes = read_data(file)
        quick_data_extraction(perfumes)

    else:
        file = '../data/perfume_data.json'
        perfumes = read_data(file)
        quick_data_extraction(perfumes)
        sentences = clean_data(perfumes)
        model = word_2_vec(sentences)

    # training_loss = model.get_latest_training_loss()
    # print("Training loss: ", training_loss)
    example(model)


main()
