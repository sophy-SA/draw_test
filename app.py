import streamlit as st
import random
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# お題のリスト
topics = ["猫", "ファンタジーの生き物", "未来の乗り物", "風景", "絶対勝てないボスキャラ","理想の家","好きな食べ物","宇宙","かわいいロボット","犬","つねちゃんの似顔絵","お伽話から1シーン","自由にどうぞ！(当たり)","さむらい"]

# アプリのタイトル
st.title("お絵かきチャレンジ2")

# ランダムお題生成
if st.button("お題を生成"):
    topic = random.choice(topics)
    st.session_state.topic = topic

# お題の表示
if 'topic' in st.session_state:
    st.write(f"お題: {st.session_state.topic}")

# 線の色を選択するセレクトボックス
color_options = {
    "黒": "black",
    "赤": "red",
    "青": "blue",
    "緑": "green",
    "黄": "yellow",
    "紫": "purple",
    "オレンジ": "orange"
}
stroke_color = st.selectbox("線の色は変更できます:", list(color_options.keys()))

# お絵かき用キャンバス
st.write("キャンバスに絵を描いてください。")
canvas_result = st_canvas(
    fill_color="white",  # 背景色
    stroke_color=color_options[stroke_color],  # 描画色を英語に変換
    stroke_width=3,
    height=400,
    width=400,
    key="canvas"
)

# 作者名の入力
author_name = st.text_input("作者名を入力してください:")

# 作品を保存する機能
if st.button("作品を保存"):
    if canvas_result.image_data is not None:
        # gal_dataディレクトリのパスを正しく設定
        gal_data = "gal_data"
        os.makedirs(gal_data, exist_ok=True)  # ディレクトリが存在しない場合は作成

        filename = f"{author_name}_{len(os.listdir(gal_data))}.png"
        save_path = os.path.join(gal_data, filename)  # パスを正しく結合

        image = Image.fromarray(canvas_result.image_data)
        image.save(save_path)
        st.success(f"作品が保存されました！ ({author_name})")
        
        # 保存した作品の情報を表示
        if 'gallery' not in st.session_state:
            st.session_state.gallery = []
        st.session_state.gallery.append(filename)  # ファイル名のみを保存

# ギャラリー表示
st.write("保存された作品:")
gal_data = "gal_data"  # ディレクトリパスを設定
filenames = os.listdir(gal_data)
if filenames:
    for fname in filenames:
        col1, col2 = st.columns([4, 1])
        with col1:
            image_path = os.path.join(gal_data, fname)  # 画像パスを正しく結合
            st.image(image_path, caption=f"作品: {fname}", use_containr_width=True)
        with col2:
            if st.button("削除", key=fname):
                os.remove(os.path.join(gal_data, fname))  # 削除時のパスも正しく結合
                st.success(f"{fname}が削除されました。")


# 拡張案: 作品を他のユーザーと共有できる掲示板機能
# ここに掲示板機能のコードを追加できます
