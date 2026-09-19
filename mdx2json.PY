import json
import argparse
from mdxpy import mdx


def mdx_to_json(mdx_path: str, output_json_path: str, output_format: str = "kv") -> None:
    """
    mdx词库转JSON
    :param mdx_path: 输入mdx文件路径
    :param output_json_path: 输出JSON文件路径
    :param output_format: 输出格式，可选 kv(键值对)/array(对象数组)
    """
    print(f"🔍 正在加载mdx词库: {mdx_path}")
    mdx = mdx.open(mdx_path)
    total_words = len(mdx)
    print(f"📊 词库共 {total_words} 个词条，开始转换...")

    # 初始化输出容器
    if output_format == "kv":
        result = {}
    else:
        result = []

    # 遍历转换所有词条
    processed = 0
    for word, definition in mdx.items():
        word_clean = word.strip()
        def_clean = definition.strip()
        if output_format == "kv":
            result[word_clean] = def_clean
        else:
            result.append({"word": word_clean, "definition": def_clean})
        
        processed += 1
        # 每处理1万词条打印一次进度
        if processed % 10000 == 0:
            print(f"⚙️  已转换 {processed}/{total_words} 个词条")

    # 写入JSON文件
    print(f"💾 正在写入输出文件...")
    with open(output_json_path, "w", encoding="utf-8") as f:
        # 不需要缩进可以去掉indent参数减小文件体积
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 转换完成！输出文件: {output_json_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mdx词库转JSON工具")
    parser.add_argument("input_mdx", help="输入的mdx词库文件路径")
    parser.add_argument("output_json", help="输出的JSON文件路径")
    parser.add_argument(
        "--format", 
        default="kv", 
        choices=["kv", "array"], 
        help='输出格式: kv=单词:释义 键值对(默认), array=[{"word":"","definition":""}] 对象数组'
    )
    args = parser.parse_args()
    mdx_to_json(args.input_mdx, args.output_json, args.format)