from collections import UserDict



class Field:
    def __init__(self, value):
    
        self.value = value
        

    def __str__(self):
        return str(self.value)



class Title(Field):
    def __init__(self, value):
        self.value = value 


class Text(Field):
    def __init__(self, value):
        self.value = value 
 

        


class Note:
    
    def __init__(self, note, tags=None):
        if tags:
            self.title = Title(tags[0][1:])
        else:
            self.title = Title('No title')
       
        
        
        if tags:
            for i in tags:
                note = note  + i
        
        self.note = Text(note)
     

    def edit_note(self, new_text):
        self.note = Text(new_text)
        
        return f'edited note Title: {self.title.value}, Text: {self.note.value}, Tags: No tags'

    def __str__(self):
        
       tags = str(self.note).find('#')
      
       if self.title.value == 'No title':
        return f"Title: {self.title.value}, Text: {self.note.value}, Tags: No tags"
       if tags != -1:
           return f"Title: {self.title.value}, Text: {self.note.value[:tags-1]}, Tags: {self.note.value[tags:]}"
       else:
           return f"Title: {self.title.value}, Text: {self.note.value}, Tags: No tags"
                
        
           
           


class NoteBook(UserDict): 
    list_n = []
    def add_note(self,note):
       
           
        if note.title.value  == 'No title':
                self.list_n.append(note)
               
                self.data['No title'] = self.list_n


                 
        else:
             self.data[note.title.value] = note
        
        return f'added{self.data}'

         
        
    def sort_note(self):
        
        list_titles= []
        main_list = []
        for i in self.data.keys():
            list_titles.append(i)
            new_list = sorted(list_titles)

        for  i  in self.data.items():
            main_list.append(i)
            
       
        for j in main_list:
           
            for f in new_list:
                if j[0] == f:
        
                   
                   main_list.remove(j)
                   main_list.append(j)
                
              
  
        self.data.clear()
        
        for k,v in main_list:
            self.data[k] = v




        return f'sorted notes:{self.data}'
    
    

    def delete_note(self, data):
        for k,v in self.data.items():
            if type(v) == list:
                  
                for i in v:
                    
                    if  data == k:
                        self.data.pop(k)
                        return 'deleted'
                    if  data in str(i) or data == str(i):
                        
                    
                        v.remove(i)
                return 'deleted'
                        


                        
            if data == k or data == str(v):
                self.data.pop(k)
                return 'deleted'
    
            
    def find_note(self,data):
         for k,v in self.data.items():
           
            if type(v) == list:
                
                for i in v:
                    if  data == k:
                        return f'found note {(str(i))}'
                    if data in str(i):
                        
                        return(str(i))
                       
                        
            
            if data == k or data in str(v):
                
                return f'found note {(self.data.get(k))}'
 
    
         
                



    
    
    
book = NoteBook()

n = Note('Love', ['#dove', '#style'])
j = Note('love everyone')
k = Note('love eve')
q = Note('kkk', ['#aoo'])
book.add_note(n)

book.add_note(j)

book.add_note(k)

book.add_note(q)


print(book.data)

print(book.sort_note())

print(book.find_note('dove'))
 
print(n.edit_note('Peace'))

print(book.delete_note('love everyone'))

print(book.find_note('Peace'))
print(book.find_note('aoo'))

