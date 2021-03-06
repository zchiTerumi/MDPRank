import  time

from LoadData import *
from MDPRank import *

if __name__ == '__main__':

    fold = sys.argv[1]

    ###########################   Load the parameter ###########################################
    Para = yaml.load(file('Para_info.yml'))

    version = Para['version']
    model = Para['model']
    dataset = Para['dataset']
    Nfeature = Para['Nfeature']
    Learningrate = Para['Learningrate']
    Nepisode = Para['Nepisode']
    Lenepisode = Para['Lenepisode']

    ######################### Load Data ##########################################################
    Ip_info = str(yaml.load(file(os.environ['HOME']+'/.host_info.yml'))['host'])
    print Ip_info

    if Ip_info == '217':
        datafile = '/home/zengwei/data/' + dataset + '/' + fold + '/'
    else:
        datafile = '/mnt/disk1/zengwei/Data/' + dataset + '/' + fold + '/'

    train_data = LoadData(datafile+'train.txt', dataset)
    vali_data  = LoadData(datafile+'vali.txt',  dataset)
    test_data  = LoadData(datafile+'test.txt',  dataset)
    nquery = len(train_data.keys())

    Resultfile = open('ApprenticeRank/'+ Ip_info + '_'+ version + '+' + dataset + '_' + fold + '_' + model +'_'+ time.strftime("%m%d", time.localtime()),'w')
    Resultfile.write(yaml.dump(Para) + '\n')


    if model == "Imitation_10":
        learner = RL_Imi_BP(Nfeature, Learningrate, Lenepisode, Resultfile)

    if model == "Softmax_10":
        learner = RL_Softmax_BP(Nfeature, Learningrate, Lenepisode, Resultfile)

    learner.Eval(train_data, 'train')
    learner.Eval(vali_data , 'vali')
    learner.Eval(test_data , 'test')
    # np.random.seed(datetime.datetime.now().microsecond)

    for ite in range(10000):
        batch = np.random.randint(nquery,size=Nepisode)
        Queryids=[]
        for i in batch:
            Queryids.append(train_data.keys()[i])

        learner.GenEpisodes(Queryids, train_data)
        learner.UpPolicy(train_data)
        learner.Eval(train_data,'train')
        learner.Eval(vali_data,'vali')
        learner.Eval(test_data,'test')

