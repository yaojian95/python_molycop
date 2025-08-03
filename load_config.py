import configparser
from pprint import pprint

def read_grinding_config(file_path, flatten=False):  # 添加 flatten 参数
    config = configparser.ConfigParser()
    config.read(file_path)
    
    params = {}
    
    sections = ['Moly-Cop Tools TM', 'Circuit', 'Mill', 'Mill Outputs', 
                'Cyclone', 'Solids', 'Load', 'Density', 'Feed', 
                'Simulated Outputs', 'Ball Size', 
                'Selection Function Parameters', 
                'Breakage Function Parameters', 
                'Classifier Constants']
    
    for section in sections:
        if section in config:
            params[section] = dict(config.items(section))
    
    # 处理特殊格式的Feed Size Distribution
    if 'Feed Size Distribution' in config:
        feed_size = {}
        for key in config['Feed Size Distribution']:
            values = [x.strip() for x in config['Feed Size Distribution'][key].split(',')]
            mesh_data = {
                'mesh': values[0],
                'opening': values[1],
                'mid_size': values[2] if len(values) > 2 else None,
                'ton_hr': float(values[3]) if len(values) > 3 else None,
                'percent_retained': float(values[4]) if len(values) > 4 else None,
                'percent_passing': float(values[5]) if len(values) > 5 else None
            }
            feed_size[key] = mesh_data
        params['Feed Size Distribution'] = feed_size
    
    convert_types(params)

    if flatten:  # 如果 flatten 为 True，将参数展平
        flat_params = {}
        for section in params:
            if section == 'Feed Size Distribution':
                for key, value in params[section].items():
                    flat_params[key] = value
            else:
                flat_params.update(params[section])
        params = flat_params
    
    return params

def convert_types(params):
    """将字符串值转换为适当的类型"""
    for section in params:
        if section == 'Feed Size Distribution':
            continue
            
        for key, value in params[section].items():
            # 尝试转换为float
            try:
                params[section][key] = float(value)
            except ValueError:
                # 如果不是数字，保持原样
                pass
            
            # 处理百分比值
            if '%' in key and isinstance(params[section][key], str):
                params[section][key] = float(value.replace('%', '').strip())

if __name__ == '__main__':
    config_path = 'grinding_config.ini'  # 你的配置文件路径
    params = read_grinding_config(config_path)
    # print(params)
    print("Mill Effective Diameter:", params['Mill']['effective diameter (ft)'])
    print("Feedrate:", params['Feed']['feedrate (ton/hr dry)'])
    print("P80:", params['Simulated Outputs']['p80'])
    
    # 打印前5个粒度分布
    print("\nFeed Size Distribution (first 5):")
    for i in range(1, 3):
        key = f'mesh_{i}'
        print(key, params['Feed Size Distribution'][key])