# This file is part of UDPipe <http://github.com/ufal/udpipe/>.
#
# Copyright 2016 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University in Prague, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import ufal.udpipe
# ufal.udpipe.Model etc. are SWIG-magic and cannot be detected by pylint
# pylint: disable=no-member

class Model:
    def __init__(self, path):
        """Load given model."""
        self.model = ufal.udpipe.Model.load(path)
        if not self.model:
            raise Exception("Cannot load UDPipe model from file '%s'" % path)

    def tokenize(self, text):
        """Tokenize the text and return list of ufal.udpipe.Sentence-s."""
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not tokenizer:
            raise Exception("The model does not have a tokenizer")
        return self._read(text, tokenizer)

    def read(self, text, in_format):
        """Load text in the given format (conllu|horizontal|vertical) and return list of ufal.udpipe.Sentence-s."""
        input_format = ufal.udpipe.InputFormat.newInputFormat(in_format)
        if not input_format:
            raise Exception("Cannot create input format '%s'" % in_format)
        return self._read(text, input_format)

    def _read(self, text, input_format):
        input_format.setText(text)
        error = ufal.udpipe.ProcessingError()
        sentences = []

        sentence = ufal.udpipe.Sentence()
        while input_format.nextSentence(sentence, error):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()
        if error.occurred():
            raise Exception(error.message)

        return sentences

    def tag(self, sentence):
        """Tag the given ufal.udpipe.Sentence (inplace)."""
        self.model.tag(sentence, self.model.DEFAULT)

    def parse(self, sentence):
        """Parse the given ufal.udpipe.Sentence (inplace)."""
        self.model.parse(sentence, self.model.DEFAULT)

    def write(self, sentences, out_format):
        """Write given ufal.udpipe.Sentence-s in the required format (conllu|horizontal|vertical)."""

        output_format = ufal.udpipe.OutputFormat.newOutputFormat(out_format)
        output = ''
        for sentence in sentences:
            output += output_format.writeSentence(sentence)
        output += output_format.finishDocument()

        return output

# Udpipe verb to dict
model = Model('russian-syntagrus-ud-2.0-170801.udpipe')
sentences = model.tokenize("Привет всем. Алиса дура! Я сделал все. Повтори уже! Порезать лук, накрошить муки, немного накромсать")

for s in sentences:
    model.tag(s)
    model.parse(s)   
conllu = model.write(sentences,'conllu')

from conllu import parse

sentences_parse = parse(conllu)
verb_dict = {}

for sentence in sentences_parse:
	for token in sentence:
		print(token['upostag'])
		if token['upostag'] == 'VERB':
			verb_dict[token['form']] = list(sentence.metadata.values())[-1]

print(verb_dict)


def get_conllu(model_path, text):
    """
    Preprocess text using ufal.udpipe.Model and CoNLL-U Parser.

    :param model_path: path to ufal.udpipe.Model (str)
    :param text: (str)
    :return: (list of TokenLists)
    """
    model = Model(model_path)

    sentences = model.tokenize(text)

    for sentence in sentences:
        model.tag(sentence)
        model.parse(sentence)

    sentences_conllu = model.write(sentences, 'conllu')
    sentences_conllu_parsed = parse(sentences_conllu)

    return sentences_conllu_parsed


def check_brackets(bracket_num, token):
    """
    Check if a token is in brackets (or a token represents a bracket itself).

    :param bracket_num: the number of open brackets (int)
    :param token: token from the parsed CoNLL-U formatted string (OrderedDict)
    :return: bracket_num (int)
    """
    if token['form'] in '({[':
        bracket_num += 1

    elif token['form'] in ')}]':
        bracket_num -= 1

    return bracket_num


def check_verb(token):
    """
    Check if a token is a verb (participles and converbs are excluded).

    :param token: token from the parsed CoNLL-U formatted string (OrderedDict)
    :return: (bool)
    """
    if token['upostag'] == 'VERB' and \
       token['feats']['VerbForm'] != 'Part' and \
       token['feats']['VerbForm'] != 'Conv':

        return True
    return


def check_space(token):
    """
    Check if a space is needed after a token.

    :param token: token from the parsed CoNLL-U formatted string (OrderedDict)
    :return: a space or an empty string (str)
    """
    if token['misc'] and \
        ('SpaceAfter' in token['misc'].keys() or
         'SpacesAfter' in token['misc'].keys()):
        return ''
    return ' '


def split_sentences(model_path, text):
    """
    Split verbs in sentences (only in cases when the verbs are originally separated by punctuation marks).
    The sentences with subordinating conjunctions or sentences in brackets are not splitted.

    :param model_path: path to ufal.udpipe.Model (str)
    :param text: text to split (str)
    :return: a list of splitted parts of each sentence (a list of lists)

    :example:
    >>> text = 'Готовый пирог посыпать сахарной пудрой, украсить черникой. При желании, украсить посыпкой.'
    >>> print(split_sentences('russian-syntagrus-ud-2.0-170801.udpipe', text))
    [['Готовый пирог посыпать сахарной пудрой, ', 'украсить черникой. '], ['При желании, украсить посыпкой.']]

    :exceptions:
    >>> text_with_subordinating_conj = 'Если верх пирога начнет пригорать, накройте его фольгой.'
    >>> print(split_sentences('russian-syntagrus-ud-2.0-170801.udpipe', text_with_subordinating_conj))
    [['Если верх пирога начнет пригорать, накройте его фольгой.']]

    >>> text_with_part_conv = 'Посолив, добавить 3 зубчика чеснока, выдавленного через чеснокодавку.'
    >>> print(split_sentences('russian-syntagrus-ud-2.0-170801.udpipe', text_with_part_conv))
    [['Посолив, добавить 3 зубчика чеснока, выдавленного через чеснокодавку.']]

    >>> text_in_brackets = 'Форму (я использовала форму размером 25 см) немного смазать маслом.'
    >>> print(split_sentences('russian-syntagrus-ud-2.0-170801.udpipe', text_in_brackets))
    [['Форму (я использовала форму размером 25 см) немного смазать маслом.']]
    """
    conllu_sentences = get_conllu(model_path, text)
    result = []

    for sentence in conllu_sentences:

        sentence_list = ['']
        current = ''
        bracket_num = 0
        verb_in_prev = False
        verb_in_current = False
        sconj_in_sentence = False

        for token in sentence:

            current += token['form'] + check_space(token)
            bracket_num = check_brackets(bracket_num, token)

            if bracket_num:
                continue

            elif token['upostag'] == 'PUNCT':

                if verb_in_current:
                    if verb_in_prev and not sconj_in_sentence:
                        sentence_list.append(current)
                    else:
                        sentence_list[-1] += current

                    verb_in_prev = True
                    verb_in_current = False

                else:
                    sentence_list[-1] += current

                current = ''

            elif check_verb(token):
                verb_in_current = True

            elif token['upostag'] == 'SCONJ':
                sconj_in_sentence = True

        if current and (not sentence_list or sentence_list[-1] != current):
            sentence_list.append(current.strip())

        result.append(sentence_list)

    return result
