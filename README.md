# uied物体検出プロジェクト
https://github.com/MulongXie/UIED  
[こちら](https://github.com/MulongXie/UIED)を参考に開発

## インストール
$ pip install -r requirements.txt

## Usage

### 1. 学習
- ./dataset 内にフォルダ名をクラス名として画像をフォルダ毎に用意する。
- 以下を実行。

```python

$ python train_***.py 
```
  *** は、使用するモデル

### 2. 物体検出
```python
$ python run_single.py **
```
** は読み込むファイル名（拡張子を除く）

### 3. JSON->HTML/CSS変換

#### 旧バージョン

```python
$ python compile_merge_img.py **
```
** は読み込むファイル名（拡張子を除く）

- ./data/output/ip or merge or ocr 以下に結果が保存される。

#### 新規開発バージョン

```python
$ python compile_text.py **
```
** は読み込むファイル名（拡張子を除く）
(テキスト、画像を含めて変換される。)
