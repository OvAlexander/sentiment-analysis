from textblob import TextBlob

phrase = 'This is terrible. Everything is terrible and falling apart. My sentiment could not get any better in any way.'
phrase = "Today my catdog died, im in tears. Today has been a horrible day. I FUCKING hate it here. How could something so horrible happend to my poor little cat dog"
phrase = "I feel pretty hopeless about the current situation. Although we may have gotten good data, backprojection only shows one big circle. I don't know what's wrong and seems like I'm going to lose sleep tonight"
tb = TextBlob(phrase)
print(tb.sentiment)
