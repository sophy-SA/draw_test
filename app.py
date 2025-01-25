import streamlit as st
import random
import os
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import colorsys
from PIL import ImageColor

# お題のリスト
topics = ["猫", "ファンタジーの生き物", "未来の乗り物", "風景", "絶対勝てないボスキャラ","理想の家","好きな食べ物","宇宙","かわいいロボット","犬","つねちゃんの似顔絵","お伽話から1シーン","自由にどうぞ！(当たり)","さむらい"]

# アプリのタイトル
st.title("お絵かきくん")

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

# 色の選択
stroke_color = st.selectbox(
    "線色を選択",
    list(color_options.keys())
)

#未定義のデフォルト値を設定
if 'brightness' not in st.session_state:
    st.session_state.brightness = 50

if color_options[stroke_color] == "black":
    st.session_state.brightness = 10

# 明度を50に戻すボタン
if st.button("明度を50に戻す"):
    st.session_state.brightness = 50  # セッションステートに明度を保存
    # スライダーの値を直接更新するために、再実行は行わない

# 明度の調整用スライダー
brightness = st.slider(
    "明るさ調整(暗い ← → 明るい)",
    min_value=10,
    max_value=90,
    value=st.session_state.brightness,  # セッションステートから値を取得
    step=1
)

# スライダーの値をセッションステートに保存
st.session_state.brightness = brightness

# 選択された色のHSLを調整
base_color = color_options[stroke_color]
# カラーコードをRGBに変換し、HSLに変換して明度を調整
rgb = ImageColor.getrgb(base_color)
h, l, s = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
adjusted_rgb = colorsys.hls_to_rgb(h, st.session_state.brightness/100, s)
adjusted_color = f"rgb({int(adjusted_rgb[0]*255)}, {int(adjusted_rgb[1]*255)}, {int(adjusted_rgb[2]*255)})"

# お絵かき用キャンバス
#st.write("キャンバスに絵を描いてください。")

# 画面幅の80%をキャンバスの幅として設定
# canvas_width = int(st.get_viewport_width() * 0.8)

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 1)",  # 背景色を完全な白に設定
    stroke_color=adjusted_color,
    stroke_width=3,
    height=360,  # 正方形にするため、幅と同じ値を設定
    width=360,
    background_color="white",  # 追加の背景色設定
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
            st.image(image_path, caption=f"作品: {fname}", use_container_width=True)
        with col2:
            if st.button("削除", key=fname):
                os.remove(os.path.join(gal_data, fname))  # 削除時のパスも正しく結合
                st.success(f"{fname}が削除されました。")


# 拡張案: 作品を他のユーザーと共有できる掲示板機能
# ここに掲示板機能のコードを追加できます
