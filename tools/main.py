import os
import shutil
import xml.etree.ElementTree as ET
import zipfile

from PIL import Image

xml_folder = '../app/src/main/res/xml'
drawables_folder_name = 'drawable-nodpi'
miui_zoom_multiples = 0.75


def parse_xml():
    print('>>> 解析 xml 文件...\n')

    tree = ET.parse(os.path.join(xml_folder, 'appfilter.xml'))
    root = tree.getroot()

    icon_map = {}
    # Key: PackageName
    # Value: Drawable Filename

    # 获取根节点下所有 item 节点
    for item in root.findall('item'):
        component = item.get('component')
        drawable = item.get('drawable')

        # 确定是 ComponentInfo 再添加
        if component.startswith('ComponentInfo'):
            # 从 component 中提取包名
            package_name = component[component.index('{') + 1:component.index('/')]
            icon_map[package_name] = drawable

    return icon_map


def move_drawable_to_temp(map):
    print('>>> 复制 Drawable 至临时文件夹...\n')

    if os.path.exists('icons_temp'):
        shutil.rmtree('icons_temp')

    os.mkdir('icons_temp')

    for key, value in map.items():
        src_path = os.path.join(xml_folder, '..', drawables_folder_name, '%s.png') % value
        out_path = os.path.join('icons_temp', '%s.png') % key

        shutil.copyfile(src_path, out_path)


def zoom_for_miui():
    print('>>> 缩放 Drawable 到 Miui 的尺寸...\n')

    for parent, dirs, files in os.walk('icons_temp'):
        for file in files:
            print('>>> 正在转换 %s' % file)

            file_path = os.path.join('icons_temp', file)
            src_img = Image.open(file_path)

            converted_x = int(src_img.size[0] * miui_zoom_multiples)
            converted_y = int(src_img.size[1] * miui_zoom_multiples)

            offset_x = (src_img.size[0] - converted_x) / 2
            offset_y = (src_img.size[1] - converted_y) / 2

            resize_img = src_img.resize((converted_x, converted_y), Image.ANTIALIAS)

            out_img = Image.new('RGBA', src_img.size, 255)
            # 这里将 box 内的所有数据转为 int
            box = tuple(map(int, (offset_x, offset_y, converted_x + offset_x, converted_y + offset_y)))
            out_img.paste(resize_img, box)
            src_img.close()

            out_img.save(file_path)
            out_img.close()


def zip_icons():
    print('>>> 压缩图标文件...\n')

    os.chdir('icons_temp')
    zip_file = zipfile.ZipFile('../icons', mode='w')

    for parent, dirs, files in os.walk('.'):
        for file in files:
            zip_file.write(file, os.path.join('res/drawable-xxhdpi', file))

    zip_file.close()
    os.chdir('..')


def zip_miui_mtz():
    print('>>> 生成主题文件...\n')

    zip_file = zipfile.ZipFile(os.path.join(os.getcwd(), 'MBEStyle.mtz'), mode='w')
    os.chdir('resource')

    for parent, dirs, files in os.walk('.'):
        for file in files:
            if parent == '.':
                # 直接放进压缩包的文件
                zip_file.write(file)
            else:
                # 文件夹形式放入压缩包
                file_path = os.path.join(parent, file)
                arcname = file_path[1:].strip(os.path.sep)
                zip_file.write(file_path, arcname)

    os.chdir('..')
    zip_file.write('icons')

    zip_file.close()


def clean_temp_files():
    shutil.rmtree('icons_temp')
    os.remove('icons')


def auto_convert_miui():
    auto_zoom = input('是否自动缩放图标大小？(yes/no)：')

    icon_map = parse_xml()
    move_drawable_to_temp(icon_map)

    if auto_zoom == 'yes':
        zoom_for_miui()

    zip_icons()
    zip_miui_mtz()
    clean_temp_files()


def check_comoponent_repeat():
    print('\n>>> 检查中...')

    tree = ET.parse(os.path.join(xml_folder, 'appfilter.xml'))
    root = tree.getroot()

    repeat_components = {}
    # Key: ComponentInfo
    # Value: Drawables

    icon_map = {}
    for item in root.findall('item'):
        component = item.get('component')
        drawable = item.get('drawable')

        # 确定是 ComponentInfo 再添加
        if not component.startswith('ComponentInfo'): continue

        if component not in icon_map:
            icon_map[component] = drawable
        else:
            if component in repeat_components:
                # 已存在 2 个及以上重复 Drawable
                repeat_components[component].append(drawable)
            else:
                repeat_components[component] = [icon_map[component], drawable]

    for component, drawables in repeat_components.items():
        print()
        print(component)
        print('[', ', '.join(drawables), ']')


def convert_iconname_for_other():
    global xml_folder
    global drawables_folder_name

    xml_folder = input('请输入 appfilter.xml 所在的文件夹路径：')
    drawables_folder_name = 'drawable-nodpi-v4'

    icon_map = parse_xml()
    move_drawable_to_temp(icon_map)

    os.rename('icons_temp', 'converted_icons')


def get_option(options):
    while True:
        option = input('请输入你要执行的操作：')
        if option in options:
            return option
        else:
            print('输入错误，', end='')


if __name__ == '__main__':
    print('''
1. 转换 MBEStyle 图标包到 Miui 主题
2. 检查 MBEStyle 图标包 Component 信息重复
3. 为其他图标包转换图标文件名
        ''')

    option = get_option(['1', '2', '3'])

    if option == '1':
        auto_convert_miui()
    elif option == '2':
        check_comoponent_repeat()
    elif option == '3':
        convert_iconname_for_other()

    print('\n执行完成，按任意键退出')
    input()
