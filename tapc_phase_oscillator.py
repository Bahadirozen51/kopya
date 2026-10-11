import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class TAPCPhaseOscillator:
    def __init__(self, target_radius_sq=2.5):
        """
        target_radius_sq: Paylaştığınız görseldeki x^2 + y^2 = 2.5 hedef limit döngüsü katsayısı.
        Bu parametre TAPC molekülünün sinyal normalleştirme kapasitesini temsil eder.
        """
        self.r_sq = target_radius_sq

    def dynamics(self, t, state):
        x, y = state
        
        # Biyolojik Hill Fonksiyonu (Kooperatif bağlanma / doygunluk kinetiği)
        hill = (x**2) / (1.0 + x**2)
        
        # Tam olarak paylaştığınız tahta üzerindeki özgün faz denklemi
        dx_dt = y
        dy_dt = -x + (self.r_sq - x**2 - y**2) * y * hill
        
        return [dx_dt, dy_dt]

    def simulate(self, x0, y0, t_end=100, num_points=2000):
        t_span = (0, t_end)
        t_eval = np.linspace(0, t_end, num_points)
        
        solution = solve_ivp(
            self.dynamics, 
            t_span, 
            [x0, y0], 
            t_eval=t_eval, 
            method='RK45',
            rtol=1e-8,
            atol=1e-10
        )
        return solution

    def plot_phase_portrait(self, trajectories, filename="grafik_tapc_faz_portresi.png"):
        """
        Farklı başlangıç koşullarından (kanserli ve çökmüş durumlar) 
        hedef limit döngüsüne yakınsamayı çizdirir.
        """
        plt.figure(figsize=(8, 8))
        
        for idx, (x0, y0) in enumerate(trajectories):
            sol = self.simulate(x0, y0)
            # Yörünge çizgileri
            plt.plot(sol.y[0], sol.y[1], label=f'Başlangıç ({x0}, {y0})', alpha=0.8)
            # Başlangıç noktaları işareti
            plt.scatter(x0, y0, color='red' if (x0**2+y0**2) > self.r_sq else 'blue', zorder=5)

        # İdeal limit döngüsünü görsel referans olarak çizdirme (x^2 + y^2 = 2.5)
        theta = np.linspace(0, 2*np.pi, 200)
        r = np.sqrt(self.r_sq)
        plt.plot(r*np.cos(theta), r*np.sin(theta), 'k--', linewidth=2, label=f'Sağlıklı Döngü ($r^2={self.r_sq}$)')

        plt.title("TAPC Akıllı Yönlendirici Modeli - Faz Uzayı Normalizasyonu")
        plt.xlabel("Sinyal Aktivasyonu (x)")
        plt.ylabel("Değişim Hızı / Momentum (y)")
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(loc='upper right')
        plt.axis('equal')
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"[✓] Simülasyon grafiği başarıyla kaydedildi: {filename}")

if __name__ == "__main__":
    oscillator = TAPCPhaseOscillator()
    
    # Test senaryoları: 
    # (4, 4) -> Yoğun kanser gürültüsüyle gelen dış yörünge
    # (0.1, 0.1) -> Sinyali çökmüş iç yörünge
    test_yoringeler = [(4.0, 4.0), (0.1, 0.1), (-3.0, 2.0)]
    
    oscillator.plot_phase_portrait(test_yoringeler)
