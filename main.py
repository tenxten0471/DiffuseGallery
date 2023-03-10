import os
import json
import datetime
import shutil
# import asyncio
import functools
from multiprocessing import Process

from diffusers.models import AutoencoderKL, UNet2DConditionModel
from diffusers import StableDiffusionPipeline
from diffusers import (
	DDIMScheduler,
	DPMSolverSinglestepScheduler,
	DPMSolverMultistepScheduler,
	HeunDiscreteScheduler,
	KDPM2DiscreteScheduler,
	KDPM2AncestralDiscreteScheduler,
	EulerDiscreteScheduler,
	EulerAncestralDiscreteScheduler,
	)

schedulers = {
	'ddim'                   : DDIMScheduler,
	'singlestep_dpm_solver'  : DPMSolverSinglestepScheduler,
	'multistep_dpm_solver'   : DPMSolverMultistepScheduler,
	'heun'                   : HeunDiscreteScheduler,
	'dpm_discrete'           : KDPM2DiscreteScheduler,
	'dpm_discrete_ancestral' : KDPM2AncestralDiscreteScheduler,
	'euler'                  : EulerDiscreteScheduler,
	'euler_ancestral'        : EulerAncestralDiscreteScheduler,
}

import torch

from PIL import Image
import webview

class File:
	def __init__(self, path, default = None, overlay = False):
		self.path = path
		if os.path.exists(self.path) and not overlay:
			with open(self.path) as f:
				self.load()
		else:
			self.data = default
			if self.data is not None:
				self.save()
	
	def load(self):
		_, ext = os.path.splitext(self.path)
		if os.path.exists(self.path):
			with open(self.path) as f:
				if ext == '.json':
					self.data = json.load(f)
				else:
					self.data = f.read()
		else:
			raise Exception('file not found')
	
	def save(self, **kwargs):
		dirname = os.path.dirname(self.path)
		if not os.path.isdir(dirname) and dirname != '':
			os.makedirs(dirname)

		# if data is not None:
		# 	self.data = data
		self.data.update(**kwargs)
		_, ext = os.path.splitext(self.path)
		with open(self.path, 'wt') as f:
			if ext == '.json':
				json.dump(self.data, f, ensure_ascii=False, indent = 2)
			else:
				f.write(self.data)
	
	def __getitem__(self, item):
		return self.data[item]


def window_alert(window,text):
	window.evaluate_js(
		"""
		alert('{}');
		""".format(text)
		)

def window_confirm(window,text):
	result = window.evaluate_js(
		"""
		var result = window.confirm('{}');
		result
		""".format(text)
	)
	return result


class Api:
	def __init__(self, window, generator, config, generate_config):
		self.name = "js_api"
		self.gen_process = False
		self.device = 'cuda'
		self.config = config
		self.generate_config = generate_config
		self.window = window
		self.generator = generator
		
	def image_generate(self, generate_config):
		print('get_request_generate')

		if self.gen_process:
			window_alert(self.window, 'model is busy')
			return
		self.gen_process = True

		def _step_callback(step, timestep, latents):
			self.window.evaluate_js(
				"""
				set_meter_func({}, {})
				""".format(1000-(int(timestep.cpu())-1), 1000)
			)

		generate_config['callback'] = _step_callback
		generate_config['num_inference_steps'] = int(generate_config['num_inference_steps'])
		generate_config['width'] = int(generate_config['width'])
		generate_config['height'] = int(generate_config['height'])

		def _callback(images, generate_config):
			print(images, generate_config)
			dirname = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
			os.makedirs(os.path.join('web',self.config['history'], dirname))
			# del generate_config['callback']
			try:
				File(os.path.join(self.config['history'], dirname, 'generate_config.json', default = generate_config))
			except Exception as e:
				window_alert(self.window, e)
			image_data = []
			for i,image in enumerate(images):
				print(dirname)
				image_src = os.path.join(self.config['history'], dirname, '{}.png'.format(i))
				image_path = os.path.join('web',image_src)
				print(image_path)
				image.save(image_path)
				image_data.append({
					'src' : image_src,
					'path' : image_path
				})
			self.window.evaluate_js(
			"""
			generated_images_update_func({})
			""".format(image_data)
			)
			print('image_data:',image_data)

		def _error_callback(e):
			window_alert(self.window,e)
			
		self.generator.generate(**{'generate_config' : generate_config, 'callback' : _callback, 'error_callback' : _error_callback})
		
		self.gen_process = False
	
	def image_show(self, image):
		path = image['path']
		Image.open(path).show()
	
	def image_save(self, image):
		path = image['path']
		Image.open(path).show()
	
	def delete_history(self, ):
		is_delete = window_confirm(self.window, 'Delete generate history, are you sure?')
		if is_delete:
			shutil.rmtree(os.path.join('web',self.config['history']))
	
	def get_schedulers(self):
		global schedulers
		return {'selected':self.config['scheduler'],'schedulers':list(schedulers.keys())}
		
	def get_model_data(self):
		return self.config['model_list']
	
	def set_model(self, model_key, scheduler):
		print(model_key,' : ',scheduler)
		self.config.data['model_list']['selected'] = model_key
		self.config.data['scheduler'] = scheduler
		self.config.save()
		self.generator = Generator(self.config['model_list']['models'][model_key]['model_id'], scheduler, self.config['device'])

	def get_generate_config(self, config_key = None):
		if config_key is not None:
			self.generate_config.save(selected = config_key)
		return self.generate_config['configs'][self.generate_config['selected']]
	
	def get_config_data(self):
		return self.generate_config.data

	def save_generate_config(self, key, generate_config):
		self.generate_config['configs'][key] = generate_config
		self.generate_config.data['selected'] = key
		self.generate_config.save()

	def delete_generate_config(self, key):
		del self.generate_config['configs'][key]
		self.generate_config.data['selected'] = 'default'
		self.generate_config.save()

 

class WebApp:
	def __init__(self,):

		model = 'runwayml/stable-diffusion-v1-5'

		self.config = File('config.json',default = {
			'strage'    : 'strage',
			'history'   : 'history',
  			'scheduler' :'multistep_dpm_solver',
			'device'    : 'cuda',
			
			'model_list'    : {
				'selected' : os.path.basename(model),
				'models':{
					os.path.basename(model):{
						'model_id':model,
					},
				},
			},
		})

		self.generate_config = File('generate_config.json',default={
			'selected':'default',
			'configs':{
				'default' : {
					'prompt':'',
					'negative_prompt':'',
					'num_inference_steps':20,
					'num_images_per_prompt':1,
					'width':448,
					'height':768,
				},
			},
		})
		
		self.generator = Generator(self.config['model_list']['models'][self.config['model_list']['selected']]['model_id'], self.config['scheduler'], self.config['device'])

		self.api = Api(None, self.generator, self.config, self.generate_config)
		self.window = webview.create_window('Hello world', url = './web/index.html', js_api=self.api)
		self.api.window = self.window


	def start(self):
		
		webview.start(debug = True)

class Generator:
	def __init__(self, model_id, scheduler, device):
		self.model_id = model_id
		self.scheduler = scheduler
		self.pipe = None
		self.device = device

	def load(self):
		try:
			global schedulers
			scheduler = schedulers[self.scheduler].from_pretrained(self.model_id, subfolder="scheduler")
			self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16, safety_checker=None).to(self.device)
		except Exception as e:
			print(e)
		# def null_safety(images, **kwargs):
		# 	return images, False
		# self.pipe.safety_checker = null_safety

	def generate(self, generate_config = {'prompt':'girl'}, callback = lambda images:images, error_callback = lambda e:print(e)):
		
		if self.pipe is None: self.load()
		generate_config['output_type'] = 'pil'

		try:
			print('try_generate')
			images = self.pipe(**generate_config).images
			callback(images, generate_config)
			return images
		except Exception as e:
			error_callback(e)
			return

if __name__ == '__main__':
	app = WebApp()
	app.start()