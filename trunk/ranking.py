def rank_by(kind, card, rack):
    diffs=[]
    small,big=-1,81
    for n in range(0,20):
        if kind=='range':
            differ=abs(n*4+2-card)
        if kind=='rack':
            differ=abs(rack[n]-card)
        diffs.append(differ)
        n+=1
    return diffs
def preserves_sort(idx,card,rack):
    if idx==0:
        return rack[0]<rack[1]
    if idx==19:
        return rack[18]<rack[19]
    return rack[idx-1]<rack[idx] and rack[idx]<rack[idx+1]
def best_sequences(rack):
    diffs=[]
    n=0
    while n<20:
        count=1
        while n+count<20 and rack[n+count]==rack[n+count-1]+1:
            count+=1
        m=0
        while m<count:
            diffs.append(count)
            m+=1
        n+=count
    return diffs
def make_dummy():
    import random
    thing=[]
    for n in range(0,20):
        m=int(random.random()*80)
        while m in thing:
            m=int(random.random()*80)
        thing.append(m)
    return thing
