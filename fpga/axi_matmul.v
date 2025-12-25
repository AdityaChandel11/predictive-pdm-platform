/* fpga/axi_matmul.v 
   Simple AXI4-Stream Hardware Multiplier for AI Acceleration
*/
module axi_matmul (
    input wire clk,
    input wire reset_n,

    // Slave Interface (Input from CPU)
    input wire [31:0] s_axis_tdata, 
    input wire s_axis_tvalid,
    output wire s_axis_tready,

    // Master Interface (Output to CPU)
    output wire [31:0] m_axis_tdata,
    output wire m_axis_tvalid,
    input wire m_axis_tready
);
    reg [31:0] product_reg;
    reg valid_reg;

    assign s_axis_tready = m_axis_tready || !valid_reg;
    assign m_axis_tvalid = valid_reg;
    assign m_axis_tdata  = product_reg;

    always @(posedge clk) begin
        if (!reset_n) begin
            valid_reg <= 1'b0;
            product_reg <= 32'b0;
        end else begin
            if (s_axis_tvalid && s_axis_tready) begin
                // Fixed-point multiplication
                product_reg <= $signed(s_axis_tdata[31:16]) * $signed(s_axis_tdata[15:0]);
                valid_reg <= 1'b1;
            end else if (m_axis_tready) begin
                valid_reg <= 1'b0;
            end
        end
    end
endmodule