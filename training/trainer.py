from core.base import MLModule
from core.decorators import track_state
from concurrent.futures import ProcessPoolExecutor
import itertools
import asyncio
from sklearn.model_selection import train_test_split

#matdiiwch 3la comments li kandiir hhh 
class Trainer(MLModule):
    def __init__(self,model_class,param_grid:dict,X_train=None,y_train=None,max_workers:int=4):
        super().__init__()
        self.error = None
        self.max_workers = max_workers
        self.model_class = model_class
        self.parm_grid = param_grid
        self.X_train = X_train
        self.y_train = y_train
        self.results = []
        self._state = "IDLE"
        self.best_model = None
        self.best_score = -1.0

    def load(self):
        if self.X_train is None or self.y_train is None : 
            raise ValueError("!!! Data Not loaded succesfully !!!")
        self.X_t, self.X_validation, self.y_t, self.y_validation = train_test_split(self.X_train, self.y_train, test_size=0.2, random_state=42)

    
    def validate(self):
        return isinstance(self.parm_grid, dict) and len(self.parm_grid) > 0 and hasattr(self, 'X_t')

    def get_status(self):
        return self._state
    
    def generate_conf(self):
        keys , values = zip(*self.parm_grid.items())
        return [dict(zip(keys,v)) for v in itertools.product(*values) ] # we add the * for lmhm bayna [[]] => []
    
    def train_model(self,params):
        try:
            model = self.model_class(**params) # because params is dictionnaire !! so we should do ** to transform it @BY_ML(Mellouki hhhhhhhhhhhhhhhh)lmhm bkhtissar {"":,"",}=> ""=val,""=bal2
            model.fit(self.X_t,self.y_t)
            score = model.score(self.X_validation,self.y_validation)
            return {"params":params,"score":score,"model":model}
        except Exception as e :
            self.error = e 
            return {"params": params, "score": -1, "error": str(e)} 
    def find_best_modul(self):
        if not self.results:
            return 
        best_res = max(self.results,key = lambda x : x["score"])
        self.best_score = best_res["score"]
        self.best_model = best_res["model"]
        print(f"Best score : {self.best_score} best model : {self.best_model}")

    @track_state
    async def run(self):
        configs = self.generate_conf()
        loop = asyncio.get_running_loop()
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            tasks = [
                loop.run_in_executor(executor, self.train_model, config) for config in configs
            ]
            self.results = await asyncio.gather(*tasks)
            
        self.find_best_modul()
        return self.best_model
    
    
