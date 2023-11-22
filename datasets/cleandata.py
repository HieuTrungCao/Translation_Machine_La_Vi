import io
import os
import re

class CleanData:
    def __init__(self,config =None):
        if config is not None:
            data_opt= config if 'train_data_location' in config else config["data"]
            self.train_data_path= data_opt['train_data_location']
            self.test_data_path= data_opt['eval_data_location']
            self.language_tuple= (data_opt["src_lang"], data_opt["trg_lang"])
        else:
            print("Could load file")
    # @staticmethod
    # def custom_split_tokenize(sentence):
    #             """Replace default tokenize
    #             """
    #             tokens = sentence.strip().split()
    #             i=0
    #             while i < len(tokens):
    #                 tk= tokens[i]
    #                 if re.search(r'\d|www|http',tk):
    #                     tokens.remove(tk)
    #                     i-=1
    #                 i+=1
    #             return tokens
    @staticmethod        
    def clean_sentence(sentence):
        special_characters ='"@#$%^*+_\/=<>'
        end_punct = ',.]>)}?!:;'
        open_punct = '({[<}'
        for char in special_characters:
            sentence = re.sub(pattern="\\"+char,repl="",string= sentence)
        #Add a space infront of puntation characters
        for char in end_punct:
            char_pattern = re.escape(char)
            sentence = re.sub(pattern=char_pattern,repl=" "+char+" ",string=sentence) 
        for char in open_punct:
            char_pattern = re.escape(char)
            sentence = re.sub(pattern=char_pattern,repl=char+" ",string=sentence) 
        #delete duplicate spaces 
        sentence = re.sub(pattern="  "+char,repl=" ",string=sentence)
      
        return sentence
        
    def clean_file(self, mode):
        data_path=''
        if mode == 'train':
            data_path = self.train_data_path
        elif mode == 'infer':
            data_path= self.test_data_path
        src_path, trg_path = tuple(os.path.expanduser(data_path + x) for x in self.language_tuple)

        clean_src_path, clean_trg_path = tuple(os.path.expanduser(data_path +"_clean"+x) for x in self.language_tuple)
        
        # special_characters ='"@#$%^*+_\/=<>'

        # end_punct = ',.?!:'
        # open_punct = '({[<}'
        #\d+\ *(nm|mm|cm|dm|km|m|kg|h|rmp|Kw|USD|EUR|NA)\b|
        punct_patt= r'\w+(.|,|:|;|!)'
        patt = r'[\Ø\″\³\¥\—\°\”\£\★\≤\Φ\Ω\≥\×\/\\\|\“\"\'\{\}\[\]\!\@\#\$\%\^\*\(\)\+\-\=\_\`\~\→\»\【\】\•\™\♦\©\±\⬆️\⬇️\–\<\>\฿\®\€]'
        with io.open(src_path, mode='r', encoding='utf-8') as src_file, \
                io.open(clean_src_path, mode='w', encoding='utf-8') as clean_src_file:
            content = src_file.read()
            #Delete special characters       
            # for char in special_characters or char in r'[1-9]':
            #     content = re.sub(pattern="\\"+char,repl="",string= content)
            # #Add a space infront of puntation characters
            # for char in end_punct:
            #     char_pattern = re.escape(char)
            #     content = re.sub(pattern=char_pattern,repl=" "+char,string=content) 
            # for char in open_punct:
            #     char_pattern = re.escape(char)
            #     content = re.sub(pattern=char_pattern,repl=char+" ",string=content) 
            #delete duplicate spaces        
            #delete all nums, special characters, punctations
            
            content = re.sub(r'(?<!\d)(?<!\.{2})([.,:;])(?=\s|$)', r' \1', content)
          
            content = re.sub(pattern= patt, repl=" ", string= content)
            content = re.sub(pattern=r" +",repl=" ",string=content)
            clean_src_file.write(content)
                
        with io.open(trg_path, mode='r', encoding='utf-8') as trg_file, \
                io.open(clean_trg_path, mode='w', encoding='utf-8') as clean_trg_file:
            content = trg_file.read()
            #Delete special characters   
            # for char in special_characters:
            #     content = re.sub(pattern="\\"+char,repl="",string= content)
            # #Add a space infront of puntation characters
            # for char in end_punct:
            #     char_pattern = re.escape(char)
            #     content = re.sub(pattern=char_pattern,repl=" "+char,string=content)
            # for char in open_punct:
            #     char_pattern = re.escape(char)
            #     content = re.sub(pattern=char_pattern,repl=char+" ",string=content)
            content = re.sub(r'(?<!\d)(?<!\.{2})([.,:;])(?=\s|$)', r' \1', content)
            content = re.sub(pattern= patt, repl=" ", string= content)
            content = re.sub(pattern=r" +",repl=" ",string=content)

            clean_trg_file.write(content)
        print("Files cleaned successfully!")