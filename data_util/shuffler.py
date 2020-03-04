import json
import os
import random


FILTER = [
    'this',
    'these',
    'those',
    'they',
    'them',
    'their',
    'which',
    'its',
    'both',
]


def generate_shuffled_data(dir, input_filename, output_filename):
    new_training_data = []

    input_filepath = os.path.join(dir, input_filename)
    with open(input_filepath) as f:
        training_data = json.load(f)
        for sample in training_data:
            if len(sample['interaction']) <= 1:
                continue
            # extend and shuffle intreaction
            old_interactions = sample['interaction']
            new_interactions = []
            for i, turn in enumerate(old_interactions):
                if i >= 1:
                    turn['utterance'] = '{} {}'.format(old_interactions[i - 1]['utterance'], turn['utterance'])
                new_interactions.append(turn)
            random.shuffle(new_interactions)
            sample['interaction'] = new_interactions
            # update final
            sample['final']['query'] = sample['interaction'][-1]['query']
            sample['final']['utterance'] = sample['interaction'][-1]['utterance']
        new_training_data.append(sample)

    output_filepath = os.path.join(dir, output_filename)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=4)


def check_eligible_sample(sample):
    for keyword in FILTER:
        capitalized_keyword = keyword.capitalize()
        for turn in sample['interaction']:
            if keyword in turn['utterance'] or capitalized_keyword in turn['utterance']:
                return False
    return True


def count_shuffleable_samples(dir, input_filename):
    input_filepath = os.path.join(dir, input_filename)
    with open(input_filepath) as f:
        training_data = json.load(f)
        print('{} out of {} training samples are eligible for naive shuffle.'.format(
            len([sample for sample in training_data if check_eligible_sample(sample)]), len(training_data)))
    # 861 out of 3034 training samples are eligible for naive shuffle.


def main():
    # generate_shuffled_data('/home/yu/Development/editsql/data/sparc', 'train.json', 'train_shuffle.json')
    count_shuffleable_samples('/home/yu/Development/editsql/data/sparc', 'train.json')


if __name__ == '__main__':
    main()