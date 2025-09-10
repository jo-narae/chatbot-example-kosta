# fix_encoding.py - CSV 인코딩 문제 해결
import pandas as pd
import os

# 현재 스크립트 디렉토리 경로
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "한국산업은행_금융 관련 용어_20151231.csv")

# cp949 인코딩으로 CSV 파일 읽기
print("📄 CSV 파일 읽기 중 (cp949 인코딩)...")
print(f"📁 파일 경로: {csv_path}")
df = pd.read_csv(csv_path, encoding="cp949")

print(f"📊 총 {len(df)} 개 행 읽기 완료")
print("📋 첫 5개 행:")
print(df.head())

# UTF-8로 저장
print("\n💾 UTF-8 인코딩으로 저장 중...")
output_path = os.path.join(current_dir, "한국산업은행_금융용어_utf8.csv")
df.to_csv(output_path, encoding="utf-8", index=False)
print(f"📁 저장 경로: {output_path}")

print("✅ UTF-8 파일 생성 완료!")
print("🔍 '트레이딩' 관련 용어 검색:")

# 트레이딩 관련 용어 찾기
trading_rows = df[df.apply(lambda row: row.astype(str).str.contains('트레이딩|Trading|포지션|Position', case=False, na=False).any(), axis=1)]
print(f"📌 관련 용어 {len(trading_rows)}개 발견:")

for idx, row in trading_rows.iterrows():
    print(f"  - {row.iloc[2] if len(row) > 2 else 'N/A'}: {str(row.iloc[3])[:100] if len(row) > 3 else 'N/A'}...")