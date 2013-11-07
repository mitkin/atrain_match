'''
Created on Oct 18, 2010

@author: a001696
'''

class OrrbStats():
    """Abstract class for accumulating statistics from atrain_match. (What does 
    orrb stand for?)"""
    
    def __init__(self, results_files=None):
        """Create an OrrbStats object with results from *results_files*."""
        self.results_files = results_files
        if self.results_files is not None:
            self.do_stats()
    
    def do_stats(self):
        """
        Calculate all statistics and put results in instance attributes (?).
        
        """
        if not self.results_files:
            raise RuntimeError("No results files")
    
    def printout(self):
        """Generate nice printout of the results."""
        raise NotImplementedError("The printout method should be implemented in"
                                  " a subclass of OrrbStat.")
    
    def write(self, filename):
        """Write printout to a file."""
        f = open(filename, 'w')
        for l in self.printout():
            f.write(l + '\n')
        f.close()
    
    def old_interface(self, modes, output_file_desc):
        """Run through stats using old interface with config.STUDIED_MONTHS, YEARS
        and so on..."""
        from glob import glob
        from config import SATELLITE, RESOLUTION, STUDIED_YEAR, STUDIED_MONTHS, MAP, MAIN_DATADIR, OUTPUT_DIR
        lines = []
        
        for mode in modes:
            self.mode = mode
            lines.append("Processing mode: %s" % self.mode)
            lines.append("")
            for i in range(len(STUDIED_MONTHS)):
                month="%s%s" %(STUDIED_YEAR[0],STUDIED_MONTHS[i])
                results_dir = "%s/Results/%s/%skm/%s/%s/%s/%s" % (MAIN_DATADIR, SATELLITE[0], RESOLUTION[0] , STUDIED_YEAR[0], STUDIED_MONTHS[i], MAP[0], self.mode)
                
                self.results_files = glob("%s/*.dat" % results_dir)
                self.do_stats()
                
                lines.append("Month is:  %s" % month)
                lines.extend(self.printout())
            lines.append("")
            lines.append("")
        
        for l in lines:
            print(l)
        
        fd=open("%s/%s_%s%s-%s%s.dat" %(OUTPUT_DIR, output_file_desc, STUDIED_YEAR[0],STUDIED_MONTHS[0],STUDIED_YEAR[-1],STUDIED_MONTHS[-1]),'w')
        for l in lines:
            fd.writelines(l + '\n')
        fd.close()