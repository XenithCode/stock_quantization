import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StockQuantAnalyzer:
    def __init__(self):
        self.stock_data = None
        self.stock_info = None
        
    def get_stock_data(self, symbol, period="1y"):
        """获取股票数据"""
        try:
            stock = yf.Ticker(symbol)
            self.stock_data = stock.history(period=period)
            self.stock_info = stock.info
            return True
        except Exception as e:
            print(f"获取股票数据失败: {e}")
            return False
    
    def calculate_technical_indicators(self):
        """计算技术指标"""
        if self.stock_data is None:
            return None
            
        df = self.stock_data.copy()
        
        # 移动平均线
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        
        # RSI指标
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD指标
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['Signal']
        
        # 布林带
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # 成交量指标
        df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_MA']
        
        return df
    
    def calculate_risk_metrics(self):
        """计算风险指标"""
        if self.stock_data is None:
            return None
            
        returns = self.stock_data['Close'].pct_change().dropna()
        
        risk_metrics = {
            'Volatility': returns.std() * np.sqrt(252),  # 年化波动率
            'Sharpe_Ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252)),  # 夏普比率
            'Max_Drawdown': self.calculate_max_drawdown(),
            'VaR_95': returns.quantile(0.05),  # 95% VaR
            'CVaR_95': returns[returns <= returns.quantile(0.05)].mean(),  # 95% CVaR
            'Skewness': returns.skew(),
            'Kurtosis': returns.kurtosis()
        }
        
        return risk_metrics
    
    def calculate_max_drawdown(self):
        """计算最大回撤"""
        cumulative = (1 + self.stock_data['Close'].pct_change()).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    def generate_signals(self):
        """生成交易信号"""
        df = self.calculate_technical_indicators()
        if df is None:
            return None
            
        signals = pd.DataFrame(index=df.index)
        
        # RSI信号
        signals['RSI_Signal'] = 0
        signals.loc[df['RSI'] < 30, 'RSI_Signal'] = 1  # 超卖买入
        signals.loc[df['RSI'] > 70, 'RSI_Signal'] = -1  # 超买卖出
        
        # MACD信号
        signals['MACD_Signal'] = 0
        signals.loc[df['MACD'] > df['Signal'], 'MACD_Signal'] = 1
        signals.loc[df['MACD'] < df['Signal'], 'MACD_Signal'] = -1
        
        # 布林带信号
        signals['BB_Signal'] = 0
        signals.loc[df['Close'] < df['BB_Lower'], 'BB_Signal'] = 1  # 价格触及下轨
        signals.loc[df['Close'] > df['BB_Upper'], 'BB_Signal'] = -1  # 价格触及上轨
        
        # 综合信号
        signals['Combined_Signal'] = signals['RSI_Signal'] + signals['MACD_Signal'] + signals['BB_Signal']
        
        return signals
    
    def plot_analysis(self, symbol):
        """绘制分析图表"""
        df = self.calculate_technical_indicators()
        signals = self.generate_signals()
        
        if df is None:
            return
            
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        
        # 价格和移动平均线
        axes[0].plot(df.index, df['Close'], label='收盘价', linewidth=2)
        axes[0].plot(df.index, df['MA5'], label='MA5', alpha=0.7)
        axes[0].plot(df.index, df['MA20'], label='MA20', alpha=0.7)
        axes[0].plot(df.index, df['MA50'], label='MA50', alpha=0.7)
        axes[0].plot(df.index, df['BB_Upper'], '--', label='布林带上轨', alpha=0.5)
        axes[0].plot(df.index, df['BB_Lower'], '--', label='布林带下轨', alpha=0.5)
        axes[0].fill_between(df.index, df['BB_Upper'], df['BB_Lower'], alpha=0.1)
        axes[0].set_title(f'{symbol} 价格分析')
        axes[0].legend()
        axes[0].grid(True)
        
        # RSI
        axes[1].plot(df.index, df['RSI'], label='RSI', color='purple')
        axes[1].axhline(y=70, color='r', linestyle='--', alpha=0.5)
        axes[1].axhline(y=30, color='g', linestyle='--', alpha=0.5)
        axes[1].set_title('RSI指标')
        axes[1].legend()
        axes[1].grid(True)
        
        # MACD
        axes[2].plot(df.index, df['MACD'], label='MACD', color='blue')
        axes[2].plot(df.index, df['Signal'], label='Signal', color='red')
        axes[2].bar(df.index, df['MACD_Histogram'], label='MACD Histogram', alpha=0.5)
        axes[2].set_title('MACD指标')
        axes[2].legend()
        axes[2].grid(True)
        
        # 成交量
        axes[3].bar(df.index, df['Volume'], alpha=0.5, label='成交量')
        axes[3].plot(df.index, df['Volume_MA'], label='成交量MA', color='red')
        axes[3].set_title('成交量分析')
        axes[3].legend()
        axes[3].grid(True)
        
        plt.tight_layout()
        plt.savefig(f'{symbol}_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def print_analysis_report(self, symbol):
        """打印分析报告"""
        if self.stock_data is None:
            print("没有数据可供分析")
            return
            
        print(f"\n{'='*50}")
        print(f"股票量化分析报告 - {symbol}")
        print(f"{'='*50}")
        
        # 基本信息
        latest = self.stock_data.iloc[-1]
        prev = self.stock_data.iloc[-2]
        pct_change = (latest['Close'] - prev['Close']) / prev['Close'] * 100
        
        print(f"\n📊 基本信息:")
        print(f"当前价格: ${latest['Close']:.2f}")
        print(f"涨跌幅: {pct_change:+.2f}%")
        print(f"最高价: ${latest['High']:.2f}")
        print(f"最低价: ${latest['Low']:.2f}")
        print(f"成交量: {latest['Volume']:,}")
        
        # 技术指标
        df = self.calculate_technical_indicators()
        if df is not None:
            latest_indicators = df.iloc[-1]
            print(f"\n📈 技术指标:")
            print(f"RSI: {latest_indicators['RSI']:.2f}")
            print(f"MACD: {latest_indicators['MACD']:.4f}")
            print(f"MA5: ${latest_indicators['MA5']:.2f}")
            print(f"MA20: ${latest_indicators['MA20']:.2f}")
            print(f"MA50: ${latest_indicators['MA50']:.2f}")
        
        # 风险指标
        risk_metrics = self.calculate_risk_metrics()
        if risk_metrics:
            print(f"\n⚠️ 风险指标:")
            print(f"年化波动率: {risk_metrics['Volatility']:.2%}")
            print(f"夏普比率: {risk_metrics['Sharpe_Ratio']:.2f}")
            print(f"最大回撤: {risk_metrics['Max_Drawdown']:.2%}")
            print(f"95% VaR: {risk_metrics['VaR_95']:.2%}")
            print(f"偏度: {risk_metrics['Skewness']:.2f}")
            print(f"峰度: {risk_metrics['Kurtosis']:.2f}")
        
        # 交易信号
        signals = self.generate_signals()
        if signals is not None:
            latest_signal = signals.iloc[-1]
            print(f"\n🎯 交易信号:")
            print(f"RSI信号: {latest_signal['RSI_Signal']}")
            print(f"MACD信号: {latest_signal['MACD_Signal']}")
            print(f"布林带信号: {latest_signal['BB_Signal']}")
            print(f"综合信号: {latest_signal['Combined_Signal']}")
            
            # 信号解释
            combined = latest_signal['Combined_Signal']
            if combined > 0:
                print("💚 买入信号")
            elif combined < 0:
                print("🔴 卖出信号")
            else:
                print("⚪ 观望信号")
        
        print(f"\n{'='*50}")

def main():
    analyzer = StockQuantAnalyzer()
    
    print("股票量化分析系统")
    print("="*50)
    
    while True:
        print("\n请选择操作:")
        print("1. 分析单只股票")
        print("2. 批量分析股票")
        print("3. 退出")
        
        choice = input("请输入选择 (1-3): ").strip()
        
        if choice == '1':
            symbol = input("请输入股票代码 (如: AAPL, 000001.SS): ").strip()
            if not symbol:
                symbol = "AAPL"
            
            if analyzer.get_stock_data(symbol):
                analyzer.print_analysis_report(symbol)
                analyzer.plot_analysis(symbol)
            else:
                print("获取股票数据失败")
                
        elif choice == '2':
            symbols_input = input("请输入股票代码列表 (用逗号分隔): ").strip()
            symbols = [s.strip() for s in symbols_input.split(',')]
            
            for symbol in symbols:
                if symbol:
                    print(f"\n分析股票: {symbol}")
                    if analyzer.get_stock_data(symbol):
                        analyzer.print_analysis_report(symbol)
                    else:
                        print(f"获取 {symbol} 数据失败")
                        
        elif choice == '3':
            print("感谢使用股票量化分析系统!")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()