from string import Template
import logging
import os
import time

from file_utils import *

logger = logging.getLogger(__name__)

lsf_template_string = '''#!/bin/bash

#BSUB -J ${jobname}
#BSUB -o ${submit_script_dir}/${jobname}.submit.out
#BSUB -e ${submit_script_dir}/${jobname}.submit.err
#BSUB -q ${queue}
#BSUB -n ${core}
#BSUB -R "span[ptile=${core}]"

export JOBNAME="${jobname}"

$user_script
'''

class ClusterProvider():
    def __init__(self,
                 label):

        self._label = label
        self.script_dir = '../scripts'

        config = file_interactor.parse_config("../config/config.yaml")
        self.queue = config['queue']
        self.core = config['core_count']

    def _write_submit_script(self, template, script_filename, job_name, configs):
        try:
            submit_script = Template(template).substitute(jobname=job_name, **configs)
            if not os.path.exists(script_filename):
                open(script_filename, 'w').close()
            with open(script_filename, 'w') as f:
                f.write(submit_script)
                print(f"write {script_filename} success")

        except Exception as e:
            print("Template : ", template)
            print("Args : ", job_name)
            print("Kwargs : ", configs)
            logger.error("Uncategorized error: %s", e)
            raise e

        return True
    
class LSFProvider(ClusterProvider):
    def __init__(self):
        label = 'LSF'
        super().__init__(label)

    def submit(self, command, job_name="lsf"):
        job_name = "{0}.{1}".format(job_name, time.time())

        script_path = "{0}/{1}.submit".format(self.script_dir, job_name)
        script_path = os.path.abspath(script_path)

        job_config = {}
        job_config["submit_script_dir"] = self.script_dir
        job_config["user_script"] = command
        job_config["queue"] = self.queue
        job_config["core"] = self.core

        logger.debug("Writing submit script")
        self._write_submit_script(lsf_template_string, script_path, job_name, job_config)
        
        cmd = "bsub < {0}".format(script_path)
        os.system(cmd)
        