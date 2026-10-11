import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class TAPCControlledSystem:
    def __init__(self, binding_affinity_kd=0.5, control_gain=1.2):
        """
        binding_affinity_kd: Tasarlanan molekülün hedef proteine (mutant Ras) bağlanma afinitesi (Kd).
                             Düşük Kd, yüksek bağlanma gücü demektir.
        control_gain: Molekülün sistemsel sönümlemeye uyguladığı kontrol katsayısı.
        """
        self.kd = binding_affinity_kd
        self.gain = control_gain
        self.target_radius_sq = 2.5 # Sağlıklı homeostazi çemberi ($r^2 = 2.5$)

    def controlled_dynamics(self, t, state):
        x, y = state
        
        # 1. Biyolojik Hill Fonksiyonu (Enzim doygunluk kinetiği)
        hill_term = (x**2) / (1.0 + x**2)
        
        # 2. Moleküler Kontrol Girdisi (U_control): 
        # Bağlanma afinitesine bağlı olarak sistemin kaotik salınımını sönümleyen dışarıdan müdahale.
        # Kd ne kadar iyise (düşükse) kontrol o kadar keskin ve kararlı olur.
        effective_affinity = 1.0 / (self.kd + 0.1)
        u_control = self.gain * effective_affinity * (self.target_radius_sq - (x**2 + y**2))
        
        # 3. Genelleştirilmiş Doğrusal Olmayan Dinamik Sistem Denklemi
        dx_dt = y
        dy_dt = -x + (u_control) * y * hill_term
        
        return [dx_dt, dy_dt]

    def simulate_treatment(self, x0, y0, t_end=60):
        t_span = (0, t_end)
        t_eval = np.linspace(0, t_end, 1500)
        
        sol = solve_ivp(
            self.controlled_dynamics, 
            t_span, 
            [x0, y0], 
            t_eval=t_eval, 
            method='RK45',
            rtol=1e-8, atol=1e-10
        )
        return sol

    def plot_therapeutic_response(self, initial_states, filename="grafik_tapc_terapötik_kontrol.png"):
        plt.figure(figsize=(9, 9))
        
        for (x0, y0) in initial_states:
            sol = self.simulate_treatment(x0, y0)
            # Yörünge çizgisi (Kanserli/Kaotik durumdan sağlıklı döngüye geçiş)
            plt.plot(sol.y[0], sol.y[1], label=f'Mutant Başlangıç ({x0}, {y0})', alpha=0.85, linewidth=1.5)
            plt.scatter([x0], [y0], color='crimson', zorder=5) # Başlangıç (Kanser şoku)

        # Hedef Sağlıklı Limit Döngüsü Çemberi
        theta = np.linspace(0, 2 * np.pi, 300)
        r_target = np.sqrt(self.target_radius_sq)
        plt.plot(r_target * np.cos(theta), r_target * np.sin(theta), 'k--', linewidth=2, label='Sağlıklı Homeostazi Çemberi')

        plt.title(f"TAPC Akıllı Yönlendirici - Afinite Tabanlı Terapötik Kontrol\n(Kd = {self.kd}, Kontrol Kazancı = {self.gain})")
        plt.xlabel("Ras-GTP Sinyal Aktivasyonu (x)")
        plt.ylabel("Momentum / Değişim Hızı (y)")
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend(loc='upper right')
        plt.axis('equal')
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"[✓] Terapötik kontrol simülasyonu başarıyla kaydedildi: {filename}")

if __name__ == "__main__":
    # Test: Yüksek gürültülü / aşırı aktif kanserli başlangıç koşulları
    kanserli_senaryolar = [(4.5, 3.5), (-4.0, -4.5), (3.0, -3.5)]
    
    controller = TAPCControlledSystem(binding_affinity_kd=0.3, control_gain=1.5)
    controller.plot_therapeutic_response(kanserli_senaryolar)
