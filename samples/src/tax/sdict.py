## SDict
## js 12/28/2010
## subclass of UserDict overwriting []:
## s[n] returns the entry correspondig to the smallest key k >= n


from collections import UserDict


class SDict(UserDict):
    def __getitem__(self, n):
        return UserDict.__getitem__(self, (min([k for k in self.keys() if k >= n])))
